from db import Database
from datetime import datetime, timedelta

def getDatabase(filen):
    return Database(filename = filen)

def setupDatabase(filen):
    db = Database(filename = filen) 
    
    #Unit coordinators
    db.insert("users",{"Name" : "ucOne","Type" : "UC","Units" : "CAB201"})
    db.insert("users",{"Name" : "ucTwo","Type" : "UC","Units" : "CAB202,CAB302"})

    #Tutors
    db.insert("users",{"Name" : "tutorOne","Type" : "Tutor","Units" : "CAB201"})
    db.insert("users",{"Name" : "tutorThree","Type" : "Tutor","Units" : "CAB302,CAB201"})
    db.insert("users",{"Name" : "tutorFour","Type" : "Tutor","Units" : "CAB201,CAB202,CAB302"})

    #Students
    db.insert("users",{"Name" : "n0000001","Type" : "Student","Units" : "CAB201"})
    db.insert("users",{"Name" : "n0000002","Type" : "Student","Units" : "CAB202"})
    db.insert("users",{"Name" : "n0000003","Type" : "Student","Units" : "CAB302"})
    db.insert("users",{"Name" : "n0000004","Type" : "Student","Units" : "CAB201,CAB202"})
    db.insert("users",{"Name" : "n0000005","Type" : "Student","Units" : "CAB201,CAB302"})
    db.insert("users",{"Name" : "n0000006","Type" : "Student","Units" : "CAB202,CAB302"})
    db.insert("users",{"Name" : "n0000007","Type" : "Student","Units" : "CAB201,CAB202,CAB302"})
    db.insert("users",{"Name" : "n0000008","Type" : "Student","Units" : "CAB202,CAB302,CAB201"})
    
    #Tutorials
    db.insert("tutorials",{"id" : "MON - 2PM - GP-S504","tutor" : 3,"unit" : "CAB201","semester" : "17SEM2" })
    db.insert("tutorials",{"id" : "TUE - 3PM - GP-S504","tutor" : 4,"unit" : "CAB201","semester" : "17SEM2" })
    db.insert("tutorials",{"id" : "THU - 10AM - GP-S513","tutor" : 5,"unit" : "CAB201","semester" : "17SEM2" })
    
    db.insert("tutorials",{"id" : "MON - 10AM - GP-P504""MON - 10AM - GP-P504","tutor" : 2,"unit" : "CAB202","semester" : "17SEM2" })
    db.insert("tutorials",{"id" : "TUE - 10AM - GP-P504","tutor" : 5,"unit" : "CAB202","semester" : "17SEM2" })
    
    db.insert("tutorials",{"id" : "WED - 3PM - GP-S504","tutor" : 5,"unit" : "CAB302","semester" : "17SEM2" })
    db.insert("tutorials",{"id" : "FRI - 2PM - GP-S504","tutor" : 4,"unit" : "CAB302","semester" : "17SEM2" })

    #For CreateSurvey tests
    today = datetime.now().weekday()       
    if today == 0:
        ID = "MON - 2PM - GP-P504"
        db.insert("tutorials",{"id" : ID,"tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
        db.insert("tutorials",{"id" : "SAT - 2PM - GP-P504","tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
    elif today == 1:
        ID = "TUE - 2PM - GP-P504"
        db.insert("tutorials",{"id" : ID,"tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
        db.insert("tutorials",{"id" : "SAT - 2PM - GP-P504","tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
    elif today == 2:
        ID = "WED - 2PM - GP-P504"
        db.insert("tutorials",{"id" : ID,"tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
        db.insert("tutorials",{"id" : "SAT - 2PM - GP-P504","tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
    elif today == 3:
        ID = "THU - 2PM - GP-P504"
        db.insert("tutorials",{"id" : ID,"tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
        db.insert("tutorials",{"id" : "SAT - 2PM - GP-P504","tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
    elif today == 4:
        ID = "FRI - 2PM - GP-P504"
        db.insert("tutorials",{"id" : ID,"tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
        db.insert("tutorials",{"id" : "SAT - 2PM - GP-P504","tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
    elif today == 5:
        ID = "SAT - 2PM - GP-P504"
        db.insert("tutorials",{"id" : ID,"tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
        db.insert("tutorials",{"id" : "MON - 2PM - GP-P504","tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
    elif today == 6:
        ID = "SUN - 2PM - GP-P504"
        db.insert("tutorials",{"id" : ID,"tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
        db.insert("tutorials",{"id" : "SAT - 2PM - GP-P504","tutor" : 3,"unit" : "CAB203","semester" : "17SEM2" })
    else:
        print("error")

    #Questions
    db.insert("questions",{"Question" : "How much are you enjoying this unit?", "Answer_type" : "Selection", 
        "Answer_text" : "1-5", "Image_links" : "None"})
    db.insert("questions",{"Question" : "How helpful do you think your tutor is to your learning?", 
        "Answer_type" : "Selection", "Answer_text" : "1-5", "Image_links" : "None"})
    db.insert("questions",{"Question" : "How organized is your tutor?", "Answer_type" : "Selection", 
        "Answer_text" : "1-5", "Image_links" : "None"})
    db.insert("questions",{"Question" : "How beneficial are the lectures to your learning?", "Answer_type" : "Selection", 
        "Answer_text" : "1-5", "Image_links" : "None"})
    db.insert("questions",{"Question" : "How organized is your lecturer?", "Answer_type" : "Selection", 
        "Answer_text" : "1-5", "Image_links" : "None"})
    
    #Surveys
    #CAB201
    valid = (datetime.now()+timedelta(minutes=30)).strftime("%H%M %d/%m/%Y")
    invalid = (datetime.now()-timedelta(minutes=30)).strftime("%H%M %d/%m/%Y")

    db.insert("surveys",{"Tutorial" : "MON - 2PM - GP-S504", "Date" : "05/06/2017", "Attendance" : 30, "Early_leavers" : "2",
        "Code" : "ABC123", "Expires" : invalid})
    db.insert("surveys",{"Tutorial" : "TUE - 3PM - GP-S504", "Date" : "06/06/2017", "Attendance" : 30, "Early_leavers" : "2",
        "Code" : "DEF456", "Expires" : valid})
    db.insert("surveys",{"Tutorial" : "THU - 10AM - GP-S513", "Date" : "08/06/2017", "Attendance" : 30, "Early_leavers" : "2",
        "Code" : "GHI789", "Expires" : "1222 08/06/2017"})

    #CAB202
    db.insert("surveys",{"Tutorial" : "MON - 10AM - GP-P504", "Date" : "05/06/2017", "Attendance" : 30, "Early_leavers" : "2",
        "Code" : "BE2Eb2", "Expires" : "1222 05/06/2017"}) 
    db.insert("surveys",{"Tutorial" : "TUE - 10AM - GP-P504", "Date" : "06/06/2017", "Attendance" : 30, "Early_leavers" : "2",
        "Code" : "by2eb6", "Expires" : "1222 06/06/2017"})

    #CAB302
    db.insert("surveys",{"Tutorial" : "WED - 3PM - GP-S504", "Date" : "07/06/2017", "Attendance" : 30, "Early_leavers" : "2",
        "Code" : "Ib3Wd3", "Expires" : "1722 07/06/2017"})
    db.insert("surveys",{"Tutorial" : "FRI - 2PM - GP-S504", "Date" : "09/06/2017", "Attendance" : 30, "Early_leavers" : "2",
        "Code" : "N@e32e", "Expires" : "1622 09/06/2017"})

    #Results
    #Student 1, CAB201
    db.insert("answers",{"Survey" : 3,"Question" : 1,"Person" : 6,"Result" : "4"})
    db.insert("answers",{"Survey" : 3,"Question" : 2,"Person" : 6,"Result" : "5"})
    db.insert("answers",{"Survey" : 3,"Question" : 3,"Person" : 6,"Result" : "4"})
    db.insert("answers",{"Survey" : 3,"Question" : 4,"Person" : 6,"Result" : "5"})
    db.insert("answers",{"Survey" : 3,"Question" : 5,"Person" : 6,"Result" : "5"})

    #Student 2, CAB202
    db.insert("answers",{"Survey" : 4,"Question" : 1,"Person" : 7,"Result" : "3"})
    db.insert("answers",{"Survey" : 4,"Question" : 2,"Person" : 7,"Result" : "2"})
    db.insert("answers",{"Survey" : 4,"Question" : 3,"Person" : 7,"Result" : "4"})
    db.insert("answers",{"Survey" : 4,"Question" : 4,"Person" : 7,"Result" : "4"})
    db.insert("answers",{"Survey" : 4,"Question" : 5,"Person" : 7,"Result" : "5"})

    #Student 3, CAB302
    db.insert("answers",{"Survey" : 6,"Question" : 1,"Person" : 8,"Result" : "4"})
    db.insert("answers",{"Survey" : 6,"Question" : 2,"Person" : 8,"Result" : "1"})
    db.insert("answers",{"Survey" : 6,"Question" : 3,"Person" : 8,"Result" : "1"})
    db.insert("answers",{"Survey" : 6,"Question" : 4,"Person" : 8,"Result" : "3"})
    db.insert("answers",{"Survey" : 6,"Question" : 5,"Person" : 8,"Result" : "2"})
    
    #Student 4, CAB201
    db.insert("answers",{"Survey" : 2,"Question" : 1,"Person" : 9,"Result" : "4"})
    db.insert("answers",{"Survey" : 2,"Question" : 2,"Person" : 9,"Result" : "3"})
    db.insert("answers",{"Survey" : 2,"Question" : 3,"Person" : 9,"Result" : "3"})
    db.insert("answers",{"Survey" : 2,"Question" : 4,"Person" : 9,"Result" : "3"})
    db.insert("answers",{"Survey" : 2,"Question" : 5,"Person" : 9,"Result" : "4"})

    #Student 4, CAB202
    db.insert("answers",{"Survey" : 5,"Question" : 1,"Person" : 9,"Result" : "4"})
    db.insert("answers",{"Survey" : 5,"Question" : 2,"Person" : 9,"Result" : "3"})
    db.insert("answers",{"Survey" : 5,"Question" : 3,"Person" : 9,"Result" : "3"})
    db.insert("answers",{"Survey" : 5,"Question" : 4,"Person" : 9,"Result" : "3"})
    db.insert("answers",{"Survey" : 5,"Question" : 5,"Person" : 9,"Result" : "4"})
    
    #Student 5, CAB201
    db.insert("answers",{"Survey" : 1,"Question" : 1,"Person" : 10,"Result" : "4"})
    db.insert("answers",{"Survey" : 1,"Question" : 2,"Person" : 10,"Result" : "3"})
    db.insert("answers",{"Survey" : 1,"Question" : 3,"Person" : 10,"Result" : "4"})
    db.insert("answers",{"Survey" : 1,"Question" : 4,"Person" : 10,"Result" : "3"})
    db.insert("answers",{"Survey" : 1,"Question" : 5,"Person" : 10,"Result" : "4"})

    #Student 5, CAB302
    db.insert("answers",{"Survey" : 7,"Question" : 1,"Person" : 10,"Result" : "3"})
    db.insert("answers",{"Survey" : 7,"Question" : 2,"Person" : 10,"Result" : "3"})
    db.insert("answers",{"Survey" : 7,"Question" : 3,"Person" : 10,"Result" : "3"})
    db.insert("answers",{"Survey" : 7,"Question" : 4,"Person" : 10,"Result" : "3"})
    db.insert("answers",{"Survey" : 7,"Question" : 5,"Person" : 10,"Result" : "3"})
    
    #Student 6, CAB202
    db.insert("answers",{"Survey" : 4,"Question" : 1,"Person" : 11,"Result" : "1"})
    db.insert("answers",{"Survey" : 4,"Question" : 2,"Person" : 11,"Result" : "1"})
    db.insert("answers",{"Survey" : 4,"Question" : 3,"Person" : 11,"Result" : "1"})
    db.insert("answers",{"Survey" : 4,"Question" : 4,"Person" : 11,"Result" : "1"})
    db.insert("answers",{"Survey" : 4,"Question" : 5,"Person" : 11,"Result" : "1"})

    #Student 6, CAB302
    db.insert("answers",{"Survey" : 6,"Question" : 1,"Person" : 11,"Result" : "5"})
    db.insert("answers",{"Survey" : 6,"Question" : 2,"Person" : 11,"Result" : "5"})
    db.insert("answers",{"Survey" : 6,"Question" : 3,"Person" : 11,"Result" : "5"})
    db.insert("answers",{"Survey" : 6,"Question" : 4,"Person" : 11,"Result" : "5"})
    db.insert("answers",{"Survey" : 6,"Question" : 5,"Person" : 11,"Result" : "5"})
    
    #Student 7, CAB201
    db.insert("answers",{"Survey" : 1,"Question" : 1,"Person" : 12,"Result" : "2"})
    db.insert("answers",{"Survey" : 1,"Question" : 2,"Person" : 12,"Result" : "3"})
    db.insert("answers",{"Survey" : 1,"Question" : 3,"Person" : 12,"Result" : "4"})
    db.insert("answers",{"Survey" : 1,"Question" : 4,"Person" : 12,"Result" : "5"})
    db.insert("answers",{"Survey" : 1,"Question" : 5,"Person" : 12,"Result" : "4"})
    
    #Student 7, CAB202
    db.insert("answers",{"Survey" : 4,"Question" : 1,"Person" : 12,"Result" : "5"})
    db.insert("answers",{"Survey" : 4,"Question" : 2,"Person" : 12,"Result" : "3"})
    db.insert("answers",{"Survey" : 4,"Question" : 3,"Person" : 12,"Result" : "4"})
    db.insert("answers",{"Survey" : 4,"Question" : 4,"Person" : 12,"Result" : "3"})
    db.insert("answers",{"Survey" : 4,"Question" : 5,"Person" : 12,"Result" : "4"})

    #Student 7, CAB302
    db.insert("answers",{"Survey" : 6,"Question" : 1,"Person" : 12,"Result" : "3"})
    db.insert("answers",{"Survey" : 6,"Question" : 2,"Person" : 12,"Result" : "3"})
    db.insert("answers",{"Survey" : 6,"Question" : 3,"Person" : 12,"Result" : "2"})
    db.insert("answers",{"Survey" : 6,"Question" : 4,"Person" : 12,"Result" : "3"})
    db.insert("answers",{"Survey" : 6,"Question" : 5,"Person" : 12,"Result" : "3"})
    
    #Student 8, CAB201
    db.insert("answers",{"Survey" : 2,"Question" : 1,"Person" : 13,"Result" : "3"})
    db.insert("answers",{"Survey" : 2,"Question" : 2,"Person" : 13,"Result" : "3"})
    db.insert("answers",{"Survey" : 2,"Question" : 3,"Person" : 13,"Result" : "4"})
    db.insert("answers",{"Survey" : 2,"Question" : 4,"Person" : 13,"Result" : "5"})
    db.insert("answers",{"Survey" : 2,"Question" : 5,"Person" : 13,"Result" : "4"})
    
    #Student 8, CAB202
    db.insert("answers",{"Survey" : 5,"Question" : 1,"Person" : 13,"Result" : "2"})
    db.insert("answers",{"Survey" : 5,"Question" : 2,"Person" : 13,"Result" : "2"})
    db.insert("answers",{"Survey" : 5,"Question" : 3,"Person" : 13,"Result" : "2"})
    db.insert("answers",{"Survey" : 5,"Question" : 4,"Person" : 13,"Result" : "2"})
    db.insert("answers",{"Survey" : 5,"Question" : 5,"Person" : 13,"Result" : "2"})

    #Student 8, CAB302
    db.insert("answers",{"Survey" : 7,"Question" : 1,"Person" : 13,"Result" : "4"})
    db.insert("answers",{"Survey" : 7,"Question" : 2,"Person" : 13,"Result" : "4"})
    db.insert("answers",{"Survey" : 7,"Question" : 3,"Person" : 13,"Result" : "4"})
    db.insert("answers",{"Survey" : 7,"Question" : 4,"Person" : 13,"Result" : "4"})
    db.insert("answers",{"Survey" : 7,"Question" : 5,"Person" : 13,"Result" : "4"})

    #close database
    db.close()
