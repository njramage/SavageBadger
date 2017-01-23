#Imports
from Survey.db import Database
from passlib.hash import sha256_crypt



#Database file
filen = "/var/www/Survey/Survey/Badger.db"



def checkLogin(user,passwd):
    #Connect to databse
    data = Database(filename = filen)
    actual = data.retrieve('users','User',user)
    data.close()
    if actual != [] and username == actual['User'] and sha256_crypt.verify(password, actual['Pass']):
        return True
    else:
        return False



def checkUser(user, func):
    return True if func == "SEND" and user == "SBSENT" else False


def getQuestions(surveyID):
    #Connect to databse
    db = Database(filename = filen)
    questions = []
    
    #grab questions for survey
    for q in db.retrieve("questions","Survey",surveyID):
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
            db.insert("answers",{"Question" : int(ans['QuestionID']), "Person" : int(ans['PersonID']), "Result" : str(ans['result'])})
    except Exception as e:
        raise
        #close db and return failure
        db.close()
        return False

    #close db and return success
    db.close()
    return True
    


