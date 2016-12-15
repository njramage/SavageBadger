from flask import Flask, request, url_for, session, jsonify
from flask_httpauth import HTTPBasicAuth

import handler as hl

#===========Main Client=======================
#get a survey
@app.route('/getsurvey/<id>', methods=["GET"])
def getSurvey(id):
    return jsonify({"questions" : hl.getQuestions(id))

#submit answers
@app.route('/submitsurvey/', methods=["POST"])
def submitSurvey():
    answers = requests.values['Answers']
    return jsonify({"result" : hl.submit(answer)})

if __name__ == "__main__":
    #FAKE KEY
    #USE FOR TESTING ONLY
    app.secret_key = 'nwb1g382gb197qweh1o02yhhe324n2hoih41928h31824hron123h84ro1u4r'
    app.run()
