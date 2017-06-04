#Imports
from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
import random
import strings

try:
    from db import Database
except:
    from polavo.db import Database

#Database file
#filen = "/var/www/polavo/polavo/Polavo.db"
filen = "Polavo.db"

#
# General methods
#

def checkLogin(user,passwd):
    #Connect to databse
    data = Database(filename = filen)
    actual = data.retrieve('users',{'User' : user})[0]
    data.close()
    if actual != [] and user == actual['User'] and sha256_crypt.verify(passwd, actual['Pass']):
        return True
    else:
        return False

def getUserID(name):
    """
        Returns the user's ID from thier username

        name : str : the user's name or student number

        returns int User's ID or -1 if doesn't exist
    """
    #Connect to Database
    db = Database(filename = filen)

    user = data.retrieve('users',{'Name' : name})

    db.close()

    if len(user) != 1:
        return -1
    else:
        return user[0]['ID']

#
# Student Methods
#

def getQuestions(code):
    """
        Retrieves survey questions from a database 

        code : str : access code used to identify the survey

        returns tuple : 0 - Boolean status
                        1 - List of question dictonaries OR Error string
    """
    #Connect to database
    db = Database(filename = filen)

    #Get the survey from access code
    survey = db.retrieve("surveys",{"Code" : code})
    if len(survey) == 0:
        #If code doesn't exist, return false
        db.close()
        return (False,"Invalid Code")
    #Else check if code has expired
    elif datetime.now() > datetime.strptime(survey[0]["Expires"], "%Y-%m-%d %H%M"):
        return (False,"Survey has expired")

    #grab questions for survey
    cursor = db.retrieve("questions",{"Survey" : survey[0]["ID"]}) 
    for q in cursor:
        question = {"id" :q['ID'] , "question" : q['Question'] , "type" : q['Answer_type'] , "answers" : q['Answer_text'].split(","), "images" : q['Image_links'].split(",")}
        questions.append(question)

    #close db and return questions
    db.close()
    return (True,questions)
          
def submit(user, answers):
    """
        Submits a survey result into the database

        user    : string     : the users string identifier 
        answers : list(dict) : list of survey questions IDs and results


        returns True if succesfully submitted, else False
    """
    #Connect to databse
    db = Database(filename = filen)

    userID = getUserID(user)

    #Add answers to database
    try:
        for ans in answers:
            db.insert("answers",{"Question" : int(ans['QuestionID']), "Person" : int(userID), "Result" : str(ans['Result'])})
    except Exception as e:
        print(e)
        #close db and return failure
        db.close()
        return False

    #close db and return success
    db.close()
    return True

#
# Tutor methods
#

def getTutorClasses(tutor):
    """
        Returns all the tutorial classes for a particular tutor

        tutor : str : The tutor to retrieve classes for

        return list(string) list of classes for that tutor
    """
    #Connect to databse
    db = Database(filename = filen)
    
    #Get the Tutor's UserID
    userID = getUserID(tutor)

    #Get tutorials
    tutorials = db.retrieve("questions",{"Tutor" : userID, "Semester" : "17SEM2"})

    #close db
    db.close()

    return tutorials

def createSurvey(session, attendence, early):
    """
        Creates a survey entry in the database and returns the access code

        session     : str : The session the survey is for e.g. BSB112-Mon-0900-B121
        attendance  : int : Number of students who attended the class
        early       : int : Number of students who left early


        returns str access code for the survey
    """
    #Connect to databse
    db = Database(filename = filen)

    #Create survey dictonary
    survey = {"Tutorial" : session, "Attendance" : attendance, "Early_leavers" : early}

    #Generate access code
    survey["Code"] = genCode(6)

    #Calculate expiry time
    survey["Expires"] = (datetime.now() + timedelta(minutes = 30)).strftime("%Y-%m-%d %H%M")

    #Insert survey into the database and return the access code
    db.insert("surveys",survey)
    db.close()

    return survey["Code"]


def genCode(length):
    """
        Generates a random string to be used for survey access codes

        length : int : the length the of the code

        returns str of specified length
    """
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase string.ascii_lowercase + string.digits) for _ in range(length))


#
# Unit Coordinator classes
#

def getResults(uc):
    """
        Returns all the survey results for a unit coordinator 

        uc : string : The unit coordinator's name

        returns list of nested dictonary of survey results in the following format:
            {unit code,
                {tutorial, tutor, 
                    {survey date, [survey results] } } }  
    """
    #Connect to databse
    db = Database(filename = filen)

    #Get the UC user entry
    user = db.retrieve('users',{'Name' : uc})[0]

    #Get the UC units
    unitCodes = user['Units'].split(",") 

    #For each unit, get tutorials
    units = []
    for unit in unitCodes:
        tutorials = []
        for tute in db.retrieve("tutorials",{"Unit" : unit,"Semester" : "17SEM2"}):
            #check if UC teachs this tutorial
            if tute["Tutor"] == user["ID"]:
                continue

            #Get survey results
            surveys = db.retrieve("surveys",{"Tutorial" : tute["ID"]}) 
            for survey in surveys:
                survey["results"] = db.retrieveQuery("SELECT answers.* FROM ((answers INNER JOIN questions ON answers.Question = questions.ID) 
                                                        INNER JOIN surveys ON questions.Survey = surveys.ID) 
                                                        WHERE surveys.ID = {}".format(survey["ID"]))
                #Remove code and expiry from entry
                survey.pop("Code",None)
                survey.pop("Expires",None)
            
            #Add results to the tutorial
            tute["Surveys"] = surveys

            tutorials.append(tute)

        #add unit to the units list
        units.appened({"Code" : unit, "Tutorials" : tutorials})
   

    #Close DB
    db.close()

    #Return units
    return units
        


     





