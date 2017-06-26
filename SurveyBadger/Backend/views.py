from flask import Flask, request, url_for, session, jsonify, render_template, Response, send_from_directory, abort
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                                  as Serializer, BadSignature, SignatureExpired)
from functools import wraps
import os

try: 
    import handler as hl
except:
    import polavo.handler as hl

#declare app
app = Flask(__name__)

#Security
auth = HTTPBasicAuth()

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
        session
        return jsonify({"status" :  True, "token" : gen_token(content['username'])})
    else:
        return jsonify({"status" :  False})


#===========Web Client Endpoints=======================
#Home Page
@app.route('/', methods=["GET"])
def webClient():
    return render_template("index.html")
    #return render_template("maintenance.html")

#Perform survey
@app.route('/survey/', methods=["GET"])
#@tokenAuth
def survey():
    return render_template("index.html")

#Tutor portal
@app.route('/tutor/', methods=["GET"])
#@tokenAuth
def tutor():
    return render_template("TutorForm.html", info = hl.getTutorClasses("tutor1"))

#UC portal
@app.route('/dashboard/', methods=["GET"])
#@tokenAuth
def dashboard():
    return render_template("UnitCord.html")

#Unit editor (Unsure if needed)
@app.route('/uniteditor/', methods=["GET","POST"])
@tokenAuth
def unitEditor():
    return render_template("index.html")

#===========Backend Endpoints==================
#get a survey
@app.route('/getsurvey/<code>', methods=["GET"])
#@auth.login_required
def getSurvey(code):
    questions = hl.getQuestions(code) 
    return jsonify(questions)

#serve images
@app.route('/surveyimages/<path:filename>', methods=["GET"])
def getImage(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

#submit answers
@app.route('/submitsurvey/', methods=["POST"])
#@tokenAuth
def submitSurvey():
    content = request.get_json()
    #Web client support
    if content == None:
        content = {'answers' : request.values['answers'], 'survey': request.values['survey'], 'user' : request.values['user']}

    user = content["user"]
    survey = content["survey"]
    answers = content["answers"]

    return jsonify({"result" : hl.submit(user, survey, answers)})

#submit attendance
@app.route('/submitattendance/', methods=["POST"])
#@tokenAuth
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

#===========Web error Handling================
@app.errorhandler(500)
def page_not_found(error):
        return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(error):
        return render_template('404.html'), 404

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
    app.run(debug=True)
