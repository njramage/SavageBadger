#Imports
from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
import random
import string

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
    data = Database(filename = filename)
    actual = data.retrieve('users',{'User' : user})[0]
    data.close()
    if actual != [] and user == actual['User'] and sha256_crypt.verify(passwd, actual['Pass']):
        return True
    else:
        return False

def checkExists(table, value, filename = filen):
    """ 
        Checks if a value exists in a table

        table : str  : table to check
        value : dict : value(s) to check 

        returns True if exists, else false
    """
    db = Database(filename = filename)

    try:
        result = db.retrieve(table,value)
    except:
        db.close()
        return False

    db.close()

    if len(result) == 0:
        return False
    else:
        return True



def getUserID(name,filename = filen):
    """
        Returns the user's ID from thier username

        name : str : the user's name or student number

        returns int User's ID or -1 if doesn't exist
    """
    #Connect to Database
    db = Database(filename = filename)

    user = db.retrieve('users',{'Name' : name})

    db.close()

    if len(user) != 1:
        return -1
    else:
        return user[0]['ID']

#
# Student Methods
#

def getQuestions(code,filename = filen):
    """
        Retrieves survey questions from a database 

        code : str : access code used to identify the survey

        returns dict :  status - status of request
                        survey - survey id 
                        questions - List of question dictonaries 
                        error - Error string (if applicable)
    """
    #Connect to database
    db = Database(filename = filename)

    #Get the survey from access code
    survey = db.retrieve("surveys",{"Code" : code})
    if len(survey) == 0:
        #If code doesn't exist, return false
        db.close()
        return {"status" : False,"error" : "Invalid Code"}
    #Else check if code has expired
    elif datetime.now() > datetime.strptime(survey[0]["Expires"], "%H%M %d/%m/%Y"):
        return {"status" : False,"error" : "Survey has expired"}

    #grab questions for survey
    questions = []
    cursor = db.retrieve("questions") 
    for q in cursor:
        question = {"id" :q['ID'] , "question" : q['Question'] , "type" : q['Answer_type'] , "answers" : q['Answer_text'].split(","), "images" : q['Image_links'].split(",")}
        questions.append(question)

    #close db and return questions
    db.close()
    return {"status" : True, "survey" : survey[0]["ID"], "questions" : questions}
          
def submit(user, survey, answers,filename = filen):
    """
        Submits a survey result into the database

        user    : string     : the users string identifier 
        survey  : int        : the survey ID of the completed survey 
        answers : list(dict) : list of survey questions IDs and results


        returns True if succesfully submitted, else False
    """
    #Connect to databse
    db = Database(filename = filename)

    #Get userID
    userID = getUserID(user,filename)

    #Check values
    if userID == -1 or not checkExists("surveys",{"ID" : survey},filename):
        return False


    #Add answers to database
    try:
        for ans in answers:
            db.insert("answers",{"Survey" : survey, "Question" : int(ans['Question']), "Person" : userID, "Result" : str(ans['Result'])})
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

def getTutorClasses(tutor,filename = filen):
    """
        Returns all the tutorial classes for a particular tutor

        tutor : str : The tutor to retrieve classes for

        return list(string) list of classes for that tutor
    """
    #Connect to databse
    db = Database(filename = filename)
    
    #Get the Tutor's UserID
    userID = getUserID(tutor,filename)

    #Get tutorials
    tutorials = db.retrieve("tutorials",{"Tutor" : userID, "Semester" : "17SEM2"})

    #close db
    db.close()

    return tutorials

def createSurvey(session, attendance, early,filename = filen):
    """
        Creates a survey entry in the database and returns the access code

        session     : str : The session the survey is for e.g. BSB112-Mon-0900-B121
        attendance  : int : Number of students who attended the class
        early       : int : Number of students who left early


        returns str access code for the survey
    """
    #Connect to databse
    db = Database(filename = filename)
    
    #Check for errors
    try:
        if not checkExists("tutorials",{"ID" : session},filename) or isinstance(attendance, bool) or attendance <= 0 or isinstance(early, bool) or early < 0:
            return "Invalid parameters"
        elif not checkDate(session):
            return "Incorrect Day"
    except:
        return "Invalid parameters"


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

def checkDate(ID):
    """
        Checks the day of the week of the tutorial and if it's meant to be on today

        ID: str : the tutorial identifier string

        returns True if today, else False
    """
    #gets the current weekday
    today = datetime.now().weekday()

    #gets the correct weekday for tutorial
    dayStr = ID.split()[0]
    if dayStr == "MON":
        day = 0
    elif dayStr == "TUE":
        day = 1
    elif dayStr == "WED":
        day = 2
    elif dayStr == "THU":
        day = 3
    elif dayStr == "FRI":
        day = 4
    elif dayStr == "SAT":
        day = 5
    elif dayStr == "SUN":
        day = 6
    else:
        #Invalid value
        return False

    #Return comparison of weekdays
    return today == day

def genCode(length):
    """
        Generates a random string to be used for survey access codes

        length : int : the length the of the code

        returns str of specified length
    """
    try:
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))
    except:
        return ''

#
# Unit Coordinator classes
#

def getResults(uc,filename = filen):
    """
        Returns all the survey results for a unit coordinator 

        uc : string : The unit coordinator's name

        returns list of nested dictonary of survey results in the following format:
            {unit code,
                {tutorial, tutor, 
                    {survey date, [survey results] } } }  
    """
    #Connect to databse
    db = Database(filename = filename)

    #Check if user exists
    if not checkExists("users",{"Name" : uc},filename): 
        return []

    #Get the UC user entry
    user = db.retrieve('users',{'Name' : uc})[0]

    #Check if user is a uc
    if user["Type"] != "UC":
        return []

    #Get the UC units
    unitCodes = user['Units'].split(",") 

    #For each unit, get tutorials
    units = []
    for unit in unitCodes:
        tutorials = []
        for tute in db.retrieve("tutorials",{"Unit" : unit,"Semester" : "17SEM2"}):
            #check if UC teaches this tutorial
            if tute["Tutor"] == user["ID"]:
                continue

            #Get survey results
            surveys = db.retrieve("surveys",{"Tutorial" : tute["ID"]}) 
            for survey in surveys:
                survey["results"] = db.retrieve("answers",{"Survey" : survey["ID"]})
                #Remove code and expiry from entry
                survey.pop("Code",None)
                survey.pop("Expires",None)
            
            #Add results to the tutorial
            tute["Surveys"] = surveys

            tutorials.append(tute)

        #add unit to the units list
        units.append({"Code" : unit, "Tutorials" : tutorials})
   

    #Close DB
    db.close()

    #Return units
    return units
        


     





