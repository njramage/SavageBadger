import sys
import os
from shutil import copyfile
import unittest
import sqlite3
from datetime import datetime, timedelta

#Change to src directory for testing and importing
sys.path.append(os.path.abspath('..'))

import handler as hl
from db import Database

def loadDatabase(db):
    #Unit coordinators
    db.insert("users",{"Name" : "ucOne","Email" : "uc1@qut.edu.au","Type" : "UC","Units" : "CAB201"})
    db.insert("users",{"Name" : "ucTwo","Email" : "uc2@qut.edu.au","Type" : "UC","Units" : "CAB202,CAB302"})

    #Tutors
    db.insert("users",{"Name" : "tutorOne","Email" : "tutor1@qut.edu.au","Type" : "Tutor","Units" : "CAB201"})
    db.insert("users",{"Name" : "tutorThree","Email" : "tutor2@qut.edu.au","Type" : "Tutor","Units" : "CAB302,CAB201"})
    db.insert("users",{"Name" : "tutorFour","Email" : "tutor3@qut.edu.au","Type" : "Tutor","Units" : "CAB201,CAB202,CAB302"})

    #Students
    db.insert("users",{"Name" : "n0000001","Email" : "student1@qut.edu.au","Type" : "Student","Units" : "CAB201"})
    db.insert("users",{"Name" : "n0000002","Email" : "student2@qut.edu.au","Type" : "Student","Units" : "CAB202"})
    db.insert("users",{"Name" : "n0000003","Email" : "student3@qut.edu.au","Type" : "Student","Units" : "CAB302"})
    db.insert("users",{"Name" : "n0000004","Email" : "student4@qut.edu.au","Type" : "Student","Units" : "CAB201,CAB202"})
    db.insert("users",{"Name" : "n0000005","Email" : "student5@qut.edu.au","Type" : "Student","Units" : "CAB201,CAB302"})
    db.insert("users",{"Name" : "n0000006","Email" : "student6@qut.edu.au","Type" : "Student","Units" : "CAB202,CAB302"})
    db.insert("users",{"Name" : "n0000007","Email" : "student7@qut.edu.au","Type" : "Student","Units" : "CAB201,CAB202,CAB302"})
    db.insert("users",{"Name" : "n0000008","Email" : "student8@qut.edu.au","Type" : "Student","Units" : "CAB202,CAB302,CAB201"})
    
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


class HandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.filen = "Test.db"
        copyfile("Test_base.db",self.filen)
        self.db = Database(filename = self.filen) 

    def tearDown(self):
        self.db.close()
       
    #getUserID tests
    def test_getUserID_uc(self):
        ID = hl.getUserID("ucOne",self.filen)
        self.assertEqual(ID,1)
        
    def test_getUserID_tutor(self):
        ID = hl.getUserID("tutorOne",self.filen)
        self.assertEqual(ID,3)
    
    def test_getUserID_student(self):
        ID = hl.getUserID("n0000001",self.filen)
        self.assertEqual(ID,6)
    
    def test_getUserID_nonExistent(self):
        ID = hl.getUserID("test",self.filen)
        self.assertEqual(ID,-1)
    
    def test_getUserID_wrongType(self):
        ID = hl.getUserID(True,self.filen)
        self.assertEqual(ID,-1)

    #getQuestions tests
    def test_getQuestions_active(self):
        questions = hl.getQuestions("DEF456",self.filen)
        self.assertTrue(questions["status"])
        self.assertEqual(questions["survey"],2)
        self.assertEqual(len(questions["questions"]),5)
    
    def test_getQuestions_expired(self):
        questions = hl.getQuestions("ABC123",self.filen)
        self.assertFalse(questions["status"])
        self.assertEqual(questions["error"],"Survey has expired")
    
    def test_getQuestions_nonexistant(self):
        questions = hl.getQuestions("aaaaaa",self.filen)
        self.assertFalse(questions["status"])
        self.assertEqual(questions["error"],"Invalid Code")
    
    def test_getQuestions_wrongType(self):
        questions = hl.getQuestions(123456,self.filen)
        self.assertFalse(questions["status"])
        self.assertEqual(questions["error"],"Invalid Code")

    #submit tests
    def test_submit_vaild(self):
        user = "n0000001"
        survey = 3 
        answers = [{"Question" : 1,"Result" : "1"},
                   {"Question" : 2,"Result" : "2"},
                   {"Question" : 3,"Result" : "3"},
                   {"Question" : 4,"Result" : "4"},
                   {"Question" : 5,"Result" : "5"}]

        self.assertTrue(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers",{"Survey" : 3})),10)


    def test_submit_invaild_answers(self):
        user = "n0000001"
        survey = 3
        answers = [{"Ques345n" : "b34b","wfew ew" : "1"},
                   {"Question" : 2,"Rew d" : "2"},
                   {"Ques34rn" : 3,"Reef t" : "3"},
                   {"Question" : 4,"Rehreg t" : "4"},
                   {"Queewr34n" : 5,"Reer " : "5"}]

        self.assertFalse(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers",{"Survey" : 3})),5)

    def test_submit_nonexistant_user(self):
        user = "n0000222"
        survey = 3 
        answers = [{"Question" : 1,"Result" : "1"},
                   {"Question" : 2,"Result" : "2"},
                   {"Question" : 3,"Result" : "3"},
                   {"Question" : 4,"Result" : "4"},
                   {"Question" : 5,"Result" : "5"}]

        self.assertFalse(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers")),75)

    def test_submit_nonexistant_survey(self):
        user = "n0000001"
        survey = 12 
        answers = [{"Question" : 1,"Result" : "1"},
                   {"Question" : 2,"Result" : "2"},
                   {"Question" : 3,"Result" : "3"},
                   {"Question" : 4,"Result" : "4"},
                   {"Question" : 5,"Result" : "5"}]

        self.assertFalse(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers")),75)

    def test_submit_no_answers(self):
        user = "n0000001"
        survey = 3 
        answers = []

        self.assertTrue(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers")),75)

    def test_submit_wrongType_user(self):
        user = True
        survey = 3
        answers = [{"Question" : 1,"Result" : "1"},
                   {"Question" : 2,"Result" : "2"},
                   {"Question" : 3,"Result" : "3"},
                   {"Question" : 4,"Result" : "4"},
                   {"Question" : 5,"Result" : "5"}]

        self.assertFalse(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers")),75)
    
    def test_submit_wrongType_survey(self):
        user = "n0000001"
        survey = "sdweew"
        answers = [{"Question" : 1,"Result" : "1"},
                   {"Question" : 2,"Result" : "2"},
                   {"Question" : 3,"Result" : "3"},
                   {"Question" : 4,"Result" : "4"},
                   {"Question" : 5,"Result" : "5"}]

        self.assertFalse(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers")),75)
        
    def test_submit_wrongType_answer(self):
        user = "n0000001"
        survey = 3
        answers = {"Question1" : 1,"Result1" : "1",
                   "Question2" : 2,"Result2" : "2",
                   "Question3" : 3,"Result3" : "3",
                   "Question4" : 4,"Result4" : "4",
                   "Question5" : 5,"Result5" : "5"}

        self.assertFalse(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers")),75)

    #checkExists tests
    def test_checkExists_student(self):
        self.assertTrue(hl.checkExists("users", {"Name":"n0000001"}, self.filen))
    
    def test_checkExists_users(self):
        self.assertTrue(hl.checkExists("users", {}, self.filen))
    
    def test_checkExists_surveys(self):
        self.assertTrue(hl.checkExists("surveys", {}, self.filen))
    
    def test_checkExists_questions(self):
        self.assertTrue(hl.checkExists("questions", {}, self.filen))
    
    def test_checkExists_answers(self):
        self.assertTrue(hl.checkExists("answers", {}, self.filen))
    
    def test_checkExists_tutorials(self):
        self.assertTrue(hl.checkExists("tutorials", {}, self.filen))
    
    def test_checkExists_nonExistent_value(self):
        self.assertFalse(hl.checkExists("users", {"Name":"huwheiued"}, self.filen))
    
    def test_checkExists_nonExistent_table(self):
        self.assertFalse(hl.checkExists("wbjwd", {"Name":"n0000001"}, self.filen))
    
    def test_checkExists_wrongvalue(self):
        self.assertFalse(hl.checkExists("users", {"Name":True}, self.filen))
    
    #getTutorClasses tests
    def test_getTutorClasses_valid(self):
        classes = hl.getTutorClasses("tutorFour",self.filen)
        self.assertEqual(len(classes),3)
        self.assertTrue("THU - 10AM - GP-S513" in [x["ID"] for x in classes])
        self.assertTrue("TUE - 10AM - GP-P504" in [x["ID"] for x in classes])
        self.assertTrue("WED - 3PM - GP-S504" in [x["ID"] for x in classes])
    
    def test_getTutorClasses_invalid(self):
        classes = hl.getTutorClasses("n0000001",self.filen)
        self.assertEqual(len(classes),0)
    
    def test_getTutorClasses_nonexistant(self):
        classes = hl.getTutorClasses("tutorTwo",self.filen)
        self.assertEqual(len(classes),0)
 
    def test_getTutorClasses_wrongType(self):
        classes = hl.getTutorClasses(1,self.filen)
        self.assertEqual(len(classes),0)
    
    #CheckDate test
    def test_checkDate_valid(self):
        #Get current weekday
        today = datetime.now().weekday()       
        if today == 0:
            ID = "MON - 2PM - GP-P504"
        elif today == 1:
            ID = "TUE - 2PM - GP-P504"
        elif today == 2:
            ID = "WED - 2PM - GP-P504"
        elif today == 3:
            ID = "THU - 2PM - GP-P504"
        elif today == 4:
            ID = "FRI - 2PM - GP-P504"
        elif today == 5:
            ID = "SAT - 2PM - GP-P504"
        elif today == 6:
            ID = "SUN - 2PM - GP-P504"

        self.assertTrue(hl.checkDate(ID))

    def test_checkDate_invalid(self):
        today = datetime.now().weekday()       
        if today == 5:
            ID = "MON - 2PM - GP-P504"
        else:
            ID = "SAT - 2PM - GP-P504"
        
        self.assertFalse(hl.checkDate(ID))

    def test_checkDate_wrongid(self):
        self.assertFalse(hl.checkDate("2PM - GP-P504 - MON"))
   
    #createSurvey tests  
    def test_createSurvey_valid(self):
        #Create a tutorial on the correct day
        today = datetime.now().weekday()       
        ID = ""
        if today == 0:
            ID = "MON - 2PM - GP-P504"
        elif today == 1:
            ID = "TUE - 2PM - GP-P504"
        elif today == 2:
            ID = "WED - 2PM - GP-P504"
        elif today == 3:
            ID = "THU - 2PM - GP-P504"
        elif today == 4:
            ID = "FRI - 2PM - GP-P504"
        elif today == 5:
            ID = "SAT - 2PM - GP-P504"
        elif today == 6:
            ID = "SUN - 2PM - GP-P504"
    
        attendance = 28
        early = 2
        self.assertEqual(len(hl.createSurvey(ID, attendance, early,self.filen)),6)

    def test_createSurvey_wrongDay(self):
        today = datetime.now().weekday()       
        ID = ""
        if today == 5:
            ID = "MON - 2PM - GP-P504"
        else:
            ID = "SAT - 2PM - GP-P504"
        
        attendance = 28
        early = 2
        self.assertEqual(hl.createSurvey(ID, attendance, early,self.filen),"Incorrect Day")
    
    def test_createSurvey_nonexistantTute(self):
        ID = "MON - 2PM - GP-P504"
        attendance = 28
        early = 2
        self.assertEqual(hl.createSurvey(ID, attendance, early,self.filen),"Invalid parameters")
    
    def test_createSurvey_invalidAttendence(self):
        #Create a tutorial on the correct day
        today = datetime.now().weekday()       
        ID = ""
        if today == 0:
            ID = "MON - 2PM - GP-P504"
        elif today == 1:
            ID = "TUE - 2PM - GP-P504"
        elif today == 2:
            ID = "WED - 2PM - GP-P504"
        elif today == 3:
            ID = "THU - 2PM - GP-P504"
        elif today == 4:
            ID = "FRI - 2PM - GP-P504"
        elif today == 5:
            ID = "SAT - 2PM - GP-P504"
        elif today == 6:
            ID = "SUN - 2PM - GP-P504"
    
        attendance = -28
        early = 2
        self.assertEqual(hl.createSurvey(ID, attendance, early,self.filen),"Invalid parameters")

    def test_createSurvey_invalidEarly(self):
        #Create a tutorial on the correct day
        today = datetime.now().weekday()       
        ID = ""
        if today == 0:
            ID = "MON - 2PM - GP-P504"
        elif today == 1:
            ID = "TUE - 2PM - GP-P504"
        elif today == 2:
            ID = "WED - 2PM - GP-P504"
        elif today == 3:
            ID = "THU - 2PM - GP-P504"
        elif today == 4:
            ID = "FRI - 2PM - GP-P504"
        elif today == 5:
            ID = "SAT - 2PM - GP-P504"
        elif today == 6:
            ID = "SUN - 2PM - GP-P504"
    
        attendance = 28
        early = -2
        self.assertEqual(hl.createSurvey(ID, attendance, early,self.filen),"Invalid parameters")

    def test_createSurvey_wrongTypeTute(self):
        ID = True 
        attendance = 28
        early = 2
        self.assertEqual(hl.createSurvey(ID, attendance, early,self.filen),"Invalid parameters")
    
    def test_createSurvey_wrongTypeAttendence(self):
        #Create a tutorial on the correct day
        today = datetime.now().weekday()       
        ID = ""
        if today == 0:
            ID = "MON - 2PM - GP-P504"
        elif today == 1:
            ID = "TUE - 2PM - GP-P504"
        elif today == 2:
            ID = "WED - 2PM - GP-P504"
        elif today == 3:
            ID = "THU - 2PM - GP-P504"
        elif today == 4:
            ID = "FRI - 2PM - GP-P504"
        elif today == 5:
            ID = "SAT - 2PM - GP-P504"
        elif today == 6:
            ID = "SUN - 2PM - GP-P504"
    
        attendance = True
        early = 2
        self.assertEqual(hl.createSurvey(ID, attendance, early,self.filen),"Invalid parameters")

    def test_createSurvey_wrongTypeEarly(self):
        #Create a tutorial on the correct day
        ID = ""
        today = datetime.now().weekday()       
        if today == 0:
            ID = "MON - 2PM - GP-P504"
        elif today == 1:
            ID = "TUE - 2PM - GP-P504"
        elif today == 2:
            ID = "WED - 2PM - GP-P504"
        elif today == 3:
            ID = "THU - 2PM - GP-P504"
        elif today == 4:
            ID = "FRI - 2PM - GP-P504"
        elif today == 5:
            ID = "SAT - 2PM - GP-P504"
        elif today == 6:
            ID = "SUN - 2PM - GP-P504"
    
        attendance = 28
        early = "adse"
        self.assertEqual(hl.createSurvey(ID, attendance, early,self.filen),"Invalid parameters")

    #genCode tests
    def test_genCode_valid(self):
        code = hl.genCode(6) 
        self.assertEqual(len(code),6)
        self.assertTrue(isinstance(code,str))

    def test_genCode_invalid(self):
        self.assertEquals(len(hl.genCode(-2)),0)

    def test_genCode_wrongType(self):
        self.assertEquals(len(hl.genCode("Asefsfd")),0)

    #getResults test
    def test_getResults_valid(self):
        results = hl.getResults("ucOne",self.filen)
        #Unit check
        self.assertEquals(len(results),1)
        #Tutorial check
        self.assertEquals(len(results[0]["Tutorials"]),3)
        #Survey check
        self.assertEquals(len(results[0]["Tutorials"][0]["Surveys"]),1)
        self.assertEquals(len(results[0]["Tutorials"][1]["Surveys"]),1)
        self.assertEquals(len(results[0]["Tutorials"][2]["Surveys"]),1)
        #Results check
        self.assertEquals(len(results[0]["Tutorials"][0]["Surveys"][0]["results"]),10)
        self.assertEquals(len(results[0]["Tutorials"][1]["Surveys"][0]["results"]),10)
        self.assertEquals(len(results[0]["Tutorials"][2]["Surveys"][0]["results"]),5)


    def test_getResults_valid_hiddenTutes(self):
        results = hl.getResults("ucTwo",self.filen)
        #Unit check
        self.assertEquals(len(results),2)
        #Tutorial check
        self.assertEquals(len(results[0]["Tutorials"]),1)
        self.assertEquals(len(results[1]["Tutorials"]),2)
        #Survey check
        self.assertEquals(len(results[0]["Tutorials"][0]["Surveys"]),1)
        self.assertEquals(len(results[1]["Tutorials"][0]["Surveys"]),1)
        self.assertEquals(len(results[1]["Tutorials"][1]["Surveys"]),1)
        #Results check
        self.assertEquals(len(results[0]["Tutorials"][0]["Surveys"][0]["results"]),10)
        self.assertEquals(len(results[1]["Tutorials"][0]["Surveys"][0]["results"]),15)
        self.assertEquals(len(results[1]["Tutorials"][1]["Surveys"][0]["results"]),10)
        
        #Additonal check to make sure UC's tute was hidden
        tutorials = [x["ID"] for x in results[0]["Tutorials"]]
        tutorials += [x["ID"] for x in results[1]["Tutorials"]]
        self.assertFalse("MON - 10AM - GP-P504" in tutorials)
        

    def test_getResults_invalid(self):
        self.assertEquals(len(hl.getResults("n0000001",self.filen)),0)

    def test_getResults_wrongType(self):
        self.assertEquals(len(hl.getResults(True,self.filen)),0)




if __name__ == '__main__':
    filen = "Test_base.db"
    try:
        os.remove(filen)
    except:
        pass
    db = Database(filename = filen)
    loadDatabase(db)
    db.close()
    unittest.main()

