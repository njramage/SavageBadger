from flask import Flask, request, url_for, session, jsonify, render_template
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                                  as Serializer, BadSignature, SignatureExpired)

import handler as hl

#declare app
app = Flask(__name__)


#Security
auth = HTTPBasicAuth()

def gen_token(user, expiration = 72000):
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

#===========Main Client=======================
#Web client
@app.route('/', methods=["GET"])
def webClient():
    return render_template("index.html")

#get a survey
@app.route('/getsurvey/<id>', methods=["GET"])
#@auth.login_required
def getSurvey(id):
    return jsonify({"questions" : hl.getQuestions(id), "token" : gen_token(id).decode('utf-8') })

#submit answers
@app.route('/submitsurvey/', methods=["POST"])
#@auth.login_required
def submitSurvey():
    #if hl.checkUser(auth.username(), "SEND"):
    content = request.get_json()
    #Web client support
    if content == None:
        content = {'token' : request.values['token'], 'answers' : request.values['answers']}
    if verify_token(content['token']):
        print("Auth succesful")
        answers = content['answers']
        return jsonify({"result" : hl.submit(answers)})
    
    print("Token auth failed")
    return jsonify({"result" : "Failed"})


if __name__ == "__main__":
    #FAKE KEY
    #USE FOR TESTING ONLY
    app.secret_key = 'nwb1g382gb197qweh1o02yhhe324n2hoih41928h31824hron123h84ro1u4r'
    app.run()
