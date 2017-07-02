from flask import Flask, request, url_for, session, jsonify, render_template, Response, send_from_directory, abort, redirect 
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
 
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                                  as Serializer, BadSignature, SignatureExpired)
from functools import wraps
import os
import redis
from datetime import timedelta

try: 
    import handler as hl
except:
    import polavo.handler as hl

#declare app and redis store
auth = HTTPBasicAuth()

store = RedisStore(redis.StrictRedis())
  
app = Flask(__name__)
KVSessionExtension(store, app)

def gen_token(user, expiration = 600):
    s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
    return s.dumps({ 'user': user })

def verify_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False # valid token, but expired
    except BadSignature:
        return False # invalid token
    
    return True

#Decorators for API
#Student login
def login_student(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'USERNAME' in session and session['USERTYPE'] == "Student":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('webClient'))
    return wrap

#Tutor and UC
def login_staff(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'USERNAME' in session and session['USERTYPE'] != "Student":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('webClient'))
    return wrap

#UC only
def login_uc(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'USERNAME' in session and session['USERTYPE'] == "UC":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('webClient'))
    return wrap

#All users for logout
def login_logout(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'USERNAME' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('webClient'))
    return wrap


@auth.verify_password
def verify_password(username, password):
    if hl.checkLogin(username, password):
        return True
    #logging.info(str(username),str(password))
    return False

def tokenAuth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if verify_token(auth.password) or verify_token(request.get_json()['token']) :
            return f(*args, **kwargs)

        return authenticate()
    return wrapper

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


#===========Authenitcation=============================
#login
@app.route('/login', methods=["POST"])
def login():
    content = request.get_json()
    #Web client support
    if content == None:
        content = {'username' : request.values['Username'], 'password' : request.values['Password']}

    if hl.checkLogin(content['username'], content['password']):
        session.permanent = True
        session["USERNAME"] = content['username']
        session["USERTYPE"] = hl.getUserType(hl.getUserID(content['username']))
        #If a UC, give them the choice of what account to login as
        status = {"status" : True}
        status["choice"] = True if session["USERTYPE"] == "UC" else False
        return jsonify(status)
    else:
        return jsonify({"status" :  False})

#logout
@app.route('/logout', methods=["GET"])
@login_logout
def logout():
    cookie_val = request.cookies.get('session').split(".")[0]
    app.permanent_session_lifetime = timedelta(seconds=1)
    store.delete(cookie_val)
    return redirect(url_for('webClient'))

#toggle UC login in as a tutor
@app.route('/tutormode', methods=["GET"])
@login_uc
def toggle():
    #Incase unseen error
    try:
        #Check check
        if "TUTORMODE" not in session:
            session["TUTORMODE"] = False
        if session["TUTORMODE"] == False:
            session["TUTORMODE"] = True
        else:
            session["TUTORMODE"] = False

        return jsonify({"status" : True})

    except:
        #clear tutor mode of safety
        session["TUTORMODE"] = None
        return jsonify({"status" :  False})


#redirect logged in users to correct portals
def login_redirect():
    #Student
    if session["USERTYPE"] == "Student":
        return redirect(url_for('survey'))
    #Tutor or UC as tutor
    elif session["USERTYPE"] == "Tutor" or (session["USERTYPE"] == "UC" and "TUTORMODE" in session):
        return redirect(url_for('tutor'))
    #UC
    elif session["USERTYPE"] == "UC":
        return redirect(url_for('dashboard'))
    #Incase there was an error, log the user out
    else:
        return redirect(url_for('logout'))

#options for html display (eg if logged in or not)
def getOptions():
    options = {}
    #check if user logged in
    if "USERNAME" in session:
        options["LoggedIn"] = True
    else:
        options["LoggedIn"] = False

    return options


#===========Web Client Endpoints=======================
#Home Page
@app.route('/', methods=["GET"])
def webClient():
    if "USERNAME" in session:
        return login_redirect()
    else:
        return render_template("index.html", options = getOptions())
    
    #return render_template("maintenance.html")

#Perform survey
@app.route('/survey/', methods=["GET"])
@login_student
def survey():
    return render_template("survey.html", options = getOptions()) 

#Tutor portal
@app.route('/tutor/', methods=["GET"])
@login_staff
def tutor():
    return render_template("TutorForm.html", info = hl.getTutorClasses(session["USERNAME"]), options = getOptions())

#UC portal
@app.route('/dashboard/', methods=["GET"])
@login_uc
def dashboard():
    return render_template("UnitCord.html", options = getOptions())

#Unit editor (Unsure if needed)
@app.route('/uniteditor/', methods=["GET","POST"])
@login_uc
def unitEditor():
    return render_template("survey.html", options = getOptions()) 

#===========Backend Endpoints==================
#get a survey
@app.route('/getsurvey/<code>', methods=["GET"])
@login_student
def getSurvey(code):
    questions = hl.getQuestions(code) 
    return jsonify(questions)

#serve images
@app.route('/surveyimages/<path:filename>', methods=["GET"])
def getImage(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

#submit answers
@app.route('/submitsurvey/', methods=["POST"])
@login_student
def submitSurvey():
    content = request.get_json()
    #Web client support
    if content == None:
        content = {'answers' : request.values['answers'], 'survey': request.values['survey']}

    user = hl.getUserID(session["USERNAME"])
    survey = content["survey"]
    answers = content["answers"]

    return jsonify({"result" : hl.submit(user, survey, answers)})

#submit attendance
@app.route('/submitattendance/', methods=["POST"])
@login_staff
def submitAttendance():
    content = request.get_json()
    #Web client support
    if content == None:
        content = {'tutorial' : request.values['tutorial'], 'attendance': request.values['attendance'], 'early' : request.values['early']}

    tutorial = content["tutorial"]
    attendance = content["attendance"]
    early = content["early"]
    
    code = hl.createSurvey(tutorial, attendance, early) 
    if code == "Invalid parameters" or code == "Incorrect Day":
        return jsonify({"status" : False, "error" : code})
    else:
        return jsonify({"status" : True, "code" : code})

# unit cordinator data
@app.route('/getresults/', methods=["GET"])
@login_uc
def unitData():
    return jsonify({"unitData": hl.getResults(session["USERNAME"])})

#===========Web error Handling================
@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html', options = {}), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', options = {}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return redirect(url_for('webClient'))

#============Legacy Endpoints=================
#create user account
@app.route('/createuser', methods=["POST"])
def createUser():
    return jsonify({"status" : True})

#===========Main Method=======================
if __name__ == "__main__":
    #FAKE KEY
    #USE FOR TESTING ONLY
    app.secret_key = 'nwb1g382gb197qweh1o02yhhe324n2hoih41928h31824hron123h84ro1u4r'
    app.config['UPLOAD_FOLDER'] = os.path.dirname(os.getcwd()+"/static/images/") 
    app.permanent_session_lifetime = timedelta(minutes=5)
    
    app.run(debug=True)
