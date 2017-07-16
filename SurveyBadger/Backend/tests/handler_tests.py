import sys
import os
from shutil import copyfile
import unittest
from datetime import datetime, timedelta

#Change to src directory for testing and importing
sys.path.append(os.path.abspath('..'))

import handler as hl
from load_testDB import setupDatabase, getDatabase
from db import Database

class HandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.filen = "Test.db"
        copyfile("Test_base.db",self.filen)
        self.db = getDatabase(self.filen)

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
    
    #getUserName tests
    def test_getUserName_uc(self):
        name = hl.getUserName(1,self.filen)
        self.assertEqual(name,"ucOne")
        
    def test_getUserName_tutor(self):
        name = hl.getUserName(3,self.filen)
        self.assertEqual(name,"tutorOne")
    
    def test_getUserName_student(self):
        name = hl.getUserName(6,self.filen)
        self.assertEqual(name,"n0000001")
    
    def test_getUserName_nonExistent(self):
        name = hl.getUserName(1002,self.filen)
        self.assertEqual(name,None)
    
    def test_getUserName_wrongType(self):
        name = hl.getUserName("efsf",self.filen)
        self.assertEqual(name,None)
    
    #getUserType tests
    def test_getUserType_uc(self):
        typ = hl.getUserType(1,self.filen)
        self.assertEqual(typ,"UC")
        
    def test_getUserType_tutor(self):
        typ = hl.getUserType(3,self.filen)
        self.assertEqual(typ,"Tutor")
    
    def test_getUserType_student(self):
        typ = hl.getUserType(6,self.filen)
        self.assertEqual(typ,"Student")
    
    def test_getUserName_nonExistent(self):
        typ = hl.getUserType(1002,self.filen)
        self.assertEqual(typ,None)
    
    def test_getUserType_wrongType(self):
        typ = hl.getUserType("efds",self.filen)
        self.assertEqual(typ,None)

    #getQuestions tests
    def test_getQuestions_active(self):
        questions = hl.getQuestions("DEF456","n0000001",self.filen)
        self.assertTrue(questions["status"])
        self.assertEqual(questions["survey"],2)
        self.assertEqual(len(questions["questions"]),5)
    
    def test_getQuestions_expired(self):
        questions = hl.getQuestions("ABC123","n0000001",self.filen)
        self.assertFalse(questions["status"])
        self.assertEqual(questions["error"],"Survey has expired")
    
    def test_getQuestions_nonexistant(self):
        questions = hl.getQuestions("aaaaaa","n0000001",self.filen)
        self.assertFalse(questions["status"])
        self.assertEqual(questions["error"],"Invalid Code")
    
    def test_getQuestions_alreadyComplete(self):
        user = "n0000002"
        survey = 2 
        answers = [{"Question" : 1,"Result" : "1"},
                   {"Question" : 2,"Result" : "2"},
                   {"Question" : 3,"Result" : "3"},
                   {"Question" : 4,"Result" : "4"},
                   {"Question" : 5,"Result" : "5"}]

        self.assertTrue(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers",{"Survey" : 2})),15)
            
        questions = hl.getQuestions("DEF456","n0000002",self.filen)
        self.assertFalse(questions["status"])
        self.assertEqual(questions["error"],"You have already completed this survey")
        

    def test_getQuestions_wrongType(self):
        questions = hl.getQuestions(123456,"n0000001",self.filen)
        self.assertFalse(questions["status"])
        self.assertEqual(questions["error"],"Invalid Code")

    #submit tests
    def test_submit_vaild(self):
        user = "n0000001"
        survey = 4 
        answers = [{"Question" : 1,"Result" : "1"},
                   {"Question" : 2,"Result" : "2"},
                   {"Question" : 3,"Result" : "3"},
                   {"Question" : 4,"Result" : "4"},
                   {"Question" : 5,"Result" : "5"}]

        self.assertTrue(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers",{"Survey" : 4})),20)

    def test_submit_multipleSubmission(self):
        user = "n0000001"
        survey = 4 
        answers = [{"Question" : 1,"Result" : "1"},
                   {"Question" : 2,"Result" : "2"},
                   {"Question" : 3,"Result" : "3"},
                   {"Question" : 4,"Result" : "4"},
                   {"Question" : 5,"Result" : "5"}]

        self.assertTrue(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers",{"Survey" : 4})),20)
        
        self.assertFalse(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers",{"Survey" : 4})),20)

    def test_submit_invaild_answers(self):
        user = "n0000001"
        survey = 4
        answers = [{"Ques345n" : "b34b","wfew ew" : "1"},
                   {"Question" : 2,"Rew d" : "2"},
                   {"Ques34rn" : 3,"Reef t" : "3"},
                   {"Question" : 4,"Rehreg t" : "4"},
                   {"Queewr34n" : 5,"Reer " : "5"}]

        self.assertFalse(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers",{"Survey" : 4})),15)

    def test_submit_nonexistant_user(self):
        user = "n0000222"
        survey = 4 
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
        survey = 4 
        answers = []

        self.assertTrue(hl.submit(user, survey, answers, self.filen))
        self.assertEqual(len(self.db.retrieve("answers")),75)

    def test_submit_wrongType_user(self):
        user = True
        survey = 4
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
        survey = 4
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
    
    #checkLogin tests
    def test_checkLogin_student(self):
        self.assertTrue(hl.checkLogin("n0000001","wordpass", self.filen))

    def test_checkLogin_tutor(self):
        self.assertTrue(hl.checkLogin("tutorOne","wordpass", self.filen))

    def test_checkLogin_uc(self):
        self.assertTrue(hl.checkLogin("ucOne","wordpass", self.filen))
    
    def test_checkLogin_nonExistent_user(self):
        self.assertFalse(hl.checkLogin("n0000500","wordpass", self.filen))

    def test_checkLogin_incorrect_password(self):
        self.assertFalse(hl.checkLogin("n0000001","password", self.filen))

    def test_checkLogin_wrong_type(self):
        self.assertFalse(hl.checkLogin(True,{"test":True}, self.filen))

    #editUserData tests
    def test_editUserData_newUser(self):
        user = {"Name" : "n0000010", "Email" : "n0000010@test.com", "Password" : "wordpass"}
        res = hl.editUserData(user, filename = self.filen)
        self.assertTrue(res['status'])
        self.assertTrue(hl.checkExists("users", {"Name":"n0000010"}, self.filen))

    def test_editUserData_updateUser(self):
        ID = hl.getUserID("n0000001",self.filen)
        user = {"ID" : ID, "Name" : "n0000001", "Password" : "newpassword"}
        res = hl.editUserData(user, True, filename = self.filen)
        self.assertTrue(res['status'])
        self.assertTrue(hl.checkExists("users", {"Name":"n0000001","Password" : "newpassword"}, self.filen))

    def test_editUserData_invalid_newUser(self):
        user = {"Name" : "n0000001", "Email" : "n0000001@test.com", "Password" : "wordpass"}
        res = hl.editUserData(user, filename = self.filen)
        self.assertFalse(res['status'])
    
    def test_editUserData_invalid_updateUser_nouser(self):
        user = {"ID" : 200, "Name" : "n0000010", "Email" : "n0000010@test.com", "Password" : "wordpass"}
        res = hl.editUserData(user, True, filename = self.filen)
        self.assertFalse(res['status'])

    def test_editUserData_invalid_updateUser_existing(self):
        ID = hl.getUserID("n0000001",self.filen)
        user = {"ID" : ID, "Name" : "n0000001", "Email" : "n0000002@test.com"}
        res = hl.editUserData(user, True, filename = self.filen)
        self.assertFalse(res['status'])

    #checkSubmitted tests
    def test_checkSubmitted_hasSubmitted(self):
        self.assertTrue(hl.checkSubmitted(6,3,self.filen))

    def test_checkSubmitted_hasNotSubmitted(self):
        self.assertFalse(hl.checkSubmitted(6,4,self.filen))

    def test_checkSubmitted_NonExistantSurvey(self):
        self.assertFalse(hl.checkSubmitted(6,100,self.filen))
    
    def test_checkSubmitted_NonExistantUser(self):
        self.assertFalse(hl.checkSubmitted(100,3,self.filen))
    
    def test_checkSubmitted_invalidSurvey(self):
        self.assertFalse(hl.checkSubmitted(6,"sdewdd",self.filen))
    
    def test_checkSubmitted_invalidUser(self):
        self.assertFalse(hl.checkSubmitted("dwedd",3,self.filen))

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
        ID = "MON - 9PM - GP-P504"
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
        self.assertEqual(len(hl.genCode(-2)),0)

    def test_genCode_wrongType(self):
        self.assertEqual(len(hl.genCode("Asefsfd")),0)

    #getResults test
    def test_getResults_valid(self):
        results = hl.getResults("ucOne",self.filen)
        #Unit check
        self.assertEqual(len(results),1)
        #Tutorial check
        self.assertEqual(len(results[0]["Tutorials"]),3)
        #Survey check
        self.assertEqual(len(results[0]["Tutorials"][0]["Surveys"]),1)
        self.assertEqual(len(results[0]["Tutorials"][1]["Surveys"]),1)
        self.assertEqual(len(results[0]["Tutorials"][2]["Surveys"]),1)
        #Results check
        self.assertEqual(len(results[0]["Tutorials"][0]["Surveys"][0]["results"]),10)
        self.assertEqual(len(results[0]["Tutorials"][1]["Surveys"][0]["results"]),10)
        self.assertEqual(len(results[0]["Tutorials"][2]["Surveys"][0]["results"]),5)


    def test_getResults_valid_hiddenTutes(self):
        results = hl.getResults("ucTwo",self.filen)
        #Unit check
        self.assertEqual(len(results),2)
        #Tutorial check
        self.assertEqual(len(results[0]["Tutorials"]),1)
        self.assertEqual(len(results[1]["Tutorials"]),2)
        #Survey check
        self.assertEqual(len(results[0]["Tutorials"][0]["Surveys"]),1)
        self.assertEqual(len(results[1]["Tutorials"][0]["Surveys"]),1)
        self.assertEqual(len(results[1]["Tutorials"][1]["Surveys"]),1)
        #Results check
        self.assertEqual(len(results[0]["Tutorials"][0]["Surveys"][0]["results"]),10)
        self.assertEqual(len(results[1]["Tutorials"][0]["Surveys"][0]["results"]),15)
        self.assertEqual(len(results[1]["Tutorials"][1]["Surveys"][0]["results"]),10)
        
        #Additonal check to make sure UC's tute was hidden
        tutorials = [x["ID"] for x in results[0]["Tutorials"]]
        tutorials += [x["ID"] for x in results[1]["Tutorials"]]
        self.assertFalse("MON - 10AM - GP-P504" in tutorials)
        

    def test_getResults_invalid(self):
        self.assertEqual(len(hl.getResults("n0000001",self.filen)),0)

    def test_getResults_wrongType(self):
        self.assertEqual(len(hl.getResults(True,self.filen)),0)




if __name__ == '__main__':
    filen = "Test_base.db"
    try:
        os.remove(filen)
    except:
        pass
    setupDatabase(filen)
    unittest.main()

