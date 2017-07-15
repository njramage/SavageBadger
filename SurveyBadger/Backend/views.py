#Std imports
import os
from datetime import timedelta

#Flask imports
import redis
from flask import Flask, request, url_for, session, jsonify, render_template, Response, send_from_directory, abort, redirect, flash 
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
from functools import wraps

#Module imports
try: 
    import handler as hl
except:
    import polavo.handler as hl

#declare app
store = RedisStore(redis.StrictRedis())
store.ttl_support = True

app = Flask(__name__)
KVSessionExtension(store,app)

#Global json responses
STATUS_TRUE = {"status" : True}
STATUS_FALSE = {"status" : False} 

#===========Authenitcation=============================
#Login required
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'LoggedIn' in session:
            return f(*args, **kwargs) 
        else:
            flash("You must be signed in first")
            return redirect(url_for("webClient"))

    return wrap

#Login student
def login_student(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'LoggedIn' in session and session['Usertype'] == "Student":
            return f(*args, **kwargs) 
        else:
            flash("You must be a student to visit this page")
            return loginRedirect()

    return wrap

#Login staff
def login_staff(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'LoggedIn' in session and session['Usertype'] != "Student":
            return f(*args, **kwargs) 
        else:
            flash("You must be a staff member to visit this page")
            return loginRedirect()

    return wrap


#Login UC 
def login_uc(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'LoggedIn' in session and session['Usertype'] == "UC":
            return f(*args, **kwargs) 
        else:
            flash("You must be a UC to visit this page")
            return loginRedirect()

    return wrap

#login redirect
def loginRedirect():
    #Not logged in
    if 'Usertype' not in session:
        return redirect(url_for("webClient")) 
    #Student
    if session['Usertype'] == "Student": 
        return redirect(url_for("survey"))
    #Tutor
    elif session['Usertype'] == "Tutor":
        return redirect(url_for("tutor"))
    #UC
    elif session['Usertype'] == "UC":
        return redirect(url_for("dashboard"))
    
#login
@app.route('/login/', methods=["POST"])
def login():
    content = request.get_json()
    #Web client support
    if content == None:
        content = {'username' : request.values['username'], 'password' : request.values['password']}

    if hl.checkLogin(content['username'], content['password']):
        session['LoggedIn'] = True
        session['Username'] = content['username']
        session['Usertype'] = hl.getUserType(hl.getUserID(content['username']))
        return jsonify(STATUS_TRUE)
    else:
        return jsonify(STATUS_FALSE)

#logout
@app.route('/logout/', methods=["GET"])
@login_required
def logout():
    cookie_val = request.cookies.get('session').split(".")[0]
    app.permanent_session_lifetime = timedelta(minutes = 1)
    session.clear()
    store.delete(cookie_val)
    flash("You have been sucessfully logged out")
    return redirect(url_for("webClient"))

#login options
def getOptions():
    options = {}
    #Login status
    options['LoggedIn'] = True if 'LoggedIn' in session and session['LoggedIn'] else False
    #UC Switch mode
    options['Switch'] = True if 'Usertype' in session and session['Usertype'] == "UC" else False
    return options

#===========Web Client Endpoints=======================
#Home Page
@app.route('/', methods=["GET","POST"])
def webClient():
    if 'LoggedIn' in session:
        return loginRedirect()

    if request.method == "POST":
        if hl.checkLogin(request.form['username'], request.form['password']):
            session['LoggedIn'] = True
            session['Username'] = request.form['username']
            session['Usertype'] = hl.getUserType(hl.getUserID(request.form['username']))
            return loginRedirect()
        else:
            return render_template("index.html", error = "Invalid username or password", options = getOptions())

    return render_template("index.html", error = "", options = getOptions())
    
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
    return render_template("TutorForm.html", info = hl.getTutorClasses(session["Username"]), options = getOptions())

#UC portal
@app.route('/dashboard/', methods=["GET"])
@login_uc
def dashboard():
    return render_template("UnitCord.html", options = getOptions())

#===========Backend Endpoints==================
#get a survey
@app.route('/getsurvey/<code>', methods=["GET"])
@login_student
def getSurvey(code):
    questions = hl.getQuestions(code,session['Username'])
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

    user = session['Username']
    survey = content["survey"]
    answers = content["answers"]
    
    result = hl.submit(user, survey, answers)
    return jsonify({"status" : result})

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
    return jsonify({"unitData": hl.getResults(session['Username'])})


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
    return jsonify(STATUS_TRUE)

#===========App config=======================
def config(key = ''):
    app.secret_key = key if key != '' else 'nwb1g382gb197qweh1o02yhhe324n2hoih41928h31824hron123h84ro1u4r'
    app.config['UPLOAD_FOLDER'] = os.path.dirname(os.getcwd()+"/static/images/")  
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)


#===========Main Method=======================
if __name__ == "__main__":
    config()
    app.run(debug=True,host='0.0.0.0')
