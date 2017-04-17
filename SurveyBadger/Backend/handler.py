#Imports
from db import Database
from passlib.hash import sha256_crypt



#Database file
#filen = "/var/www/Survey/Survey/Badger.db"
filen = "Badger.db"

def checkLogin(user,passwd):
    #Connect to databse
    data = Database(filename = filen)
    actual = data.retrieve('users','User',user)[0]
    data.close()
    if actual != [] and user == actual['User'] and sha256_crypt.verify(passwd, actual['Pass']):
        return True
    else:
        return False

def checkUser(user, func):
    return True if func == "SEND" and user == "SBSENT" else False

def getQuestions(surveyID,code = False):
    #Connect to databse
    db = Database(filename = filen)
    questions = []
    
    if code:
        if surveyID == "translink":
            cursor = db.retrieve("questions","Survey","Transpotation_Survey")
        else:
            cursor = db.retrieve("questions","Survey",surveyID)
            
    else:
        cursor = db.retrieve("questions","Survey",surveyID)

    #grab questions for survey
    for q in cursor:
        question = {"id" :q['ID'] , "question" : q['Question'] , "type" : q['Answer_type'] , "answers" : q['Answer_text'].split(",")}
        questions.append(question)

    #close db and return questions
    db.close()
    return questions
          
def submit(answers):
    #Connect to databse
    db = Database(filename = filen)
    
    #Add answers to database
    try:
        for ans in answers:
            db.insert("answers",{"Question" : int(ans['QuestionID']), "Person" : int(ans['PersonID']), "Result" : str(ans['Result'])})
    except Exception as e:
        raise
        #close db and return failure
        db.close()
        return False

    #close db and return success
    db.close()
    return True
    


