from flask import Flask, request, url_for, session, jsonify, render_template, Response
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                                  as Serializer, BadSignature, SignatureExpired)
from functools import wraps

import handler as hl

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
        if hl.checkUser(auth.username, "SEND"):
            if verify_token(auth.password):
                return f(*args, **kwargs)
        return authenticate()
    return wrapper

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

#===========Main Client=======================
#Web client
@app.route('/', methods=["GET"])
def webClient():
    return render_template("index.html")

#get a survey
@app.route('/getsurvey/<id>', methods=["GET"])
@auth.login_required
def getSurvey(id):
    return jsonify({"questions" : hl.getQuestions(id), "token" : gen_token(id).decode('utf-8') })

@app.route('/getsurveycode/', methods=["GET"])
def getFromCode():
    auth = request.authorization
    questions = hl.getQuestions(auth.password,auth.username)
    if questions == []:
        return jsonify({"status" : "Failed"})
    return jsonify({"questions" : questions, "token" : gen_token(auth.username).decode('utf-8'), "status" : "Success" })

#submit answers
@app.route('/submitsurvey/', methods=["POST"])
@tokenAuth
def submitSurvey():
    content = request.get_json()
    #Web client support
    if content == None:
        #content = {'token' : request.values['token'], 'answers' : request.values['answers']}
        content = {'answers' : request.values['answers']}
    answers = content['answers']
    return jsonify({"result" : hl.submit(answers)})


if __name__ == "__main__":
    #FAKE KEY
    #USE FOR TESTING ONLY
    app.secret_key = 'nwb1g382gb197qweh1o02yhhe324n2hoih41928h31824hron123h84ro1u4r'
    app.run()
