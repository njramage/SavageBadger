from flask import Flask, request, url_for, session, jsonify
from flask_httpauth import HTTPBasicAuth

import Survey.handler as hl

#declare app
app = Flask(__name__)


#Security
auth = HTTPBasicAuth()

#Decorators for API
@auth.verify_password
def verify_password(username, password):
    if hl.checkLogin(username, password):
        return True
    #logging.info(str(username),str(password))
    return False


#===========Main Client=======================
#get a survey
@app.route('/getsurvey/<id>', methods=["GET"])
@auth.login_required
def getSurvey(id):
    return jsonify({"questions" : hl.getQuestions(id)})

#submit answers
@app.route('/submitsurvey/', methods=["POST"])
@auth.login_required
def submitSurvey():
    answers = request.get_json()
    return jsonify({"result" : hl.submit(answers)})

if __name__ == "__main__":
    #FAKE KEY
    #USE FOR TESTING ONLY
    app.secret_key = 'nwb1g382gb197qweh1o02yhhe324n2hoih41928h31824hron123h84ro1u4r'
    app.run()
