import os
import sys
import unittest
import sqlite3

#Change to src directory for testing and importing
sys.path.append(os.path.abspath('..'))

from db import Database

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.db = Database(filename = "Test.db") 

    def tearDown(self):
        self.db.close()
        #Remove database file
        os.remove("Test.db")

    def loadTestData(self):
        self.db.insert("users",{"Name" : "testuc","Type" : "UC","Units" : "CAB202"})
        self.db.insert("users",{"Name" : "testtutor","Type" : "Tutor","Units" : "CAB201"})
        self.db.insert("users",{"Name" : "nTESTUSR","Type" : "Student","Units" : "CAB201,CAB202"})
        
        self.db.insert("tutorials",{"id" : "MON - 2PM - GP-S504","tutor" : 2,"unit" : "CAB201","semester" : "17SEM2" })
        self.db.insert("tutorials",{"id" : "TUE - 10AM - GP-P504","tutor" : 1,"unit" : "CAB202","semester" : "17SEM2" })
        
        self.db.insert("questions",{"Question" : "How much are you enjoying this unit", 
                                "Answer_type" : "Selection", "Answer_text" : "1-5", "Image_links" : "None"})
        self.db.insert("questions",{"Question" : "How helpful do you think your tutor is to your learning?", 
                                "Answer_type" : "Selection", "Answer_text" : "1-5", "Image_links" : "None"})
        
        self.db.insert("surveys",{"Tutorial" : "MON - 2PM - GP-S504","Date" : "05/06/2017","Attendance" : 30,
                                "Early_leavers" : 2,"Code" : "ABC123", "Expires" : "1622 05/06/2017"})
        self.db.insert("surveys",{"Tutorial" : "TUE - 10AM - GP-P504","Date" : "06/06/2017","Attendance" : 28,
                                "Early_leavers" : 15,"Code" : "DEF456", "Expires" : "1222 06/06/2017"})
        
        self.db.insert("answers",{"Question" : 1, "Survey" : 1, "Person" : 3,"Result" : "4"})
        self.db.insert("answers",{"Question" : 2, "Survey" : 2, "Person" : 3,"Result" : "5"})
    
    
    #Insert tests
    def test_insert_users(self):
        self.db.insert("users",{"Name" : "testuser","Type" : "Tutor","Units" : "CAB201"})
        self.assertEqual(len(self.db.retrieve("users")),1)

    def test_insert_tutorials(self):
        self.db.insert("tutorials",{"id" : "MON - 2PM - GP-S504","tutor" : 1,"unit" : "CAB201","semester" : "17SEM2" })
        self.assertEqual(len(self.db.retrieve("tutorials")),1)
    
    def test_insert_questions(self):
        self.db.insert("questions",{"Question" : "How much are you enjoying this unit", 
                                "Answer_type" : "Selection", "Answer_text" : "1-5", "Image_links" : ""})
        self.assertEqual(len(self.db.retrieve("questions")),1)
    
    def test_insert_surveys(self):
        self.db.insert("surveys",{"Tutorial" : "MON - 2PM - GP-S504","Date" : "05/06/2017","Attendance" : 30,
                                "Early_leavers" : 2,"Code" : "ABC123", "Expires" : "1622 05/06/2017"})
        self.assertEqual(len(self.db.retrieve("surveys")),1)
    
    def test_insert_answers(self):
        self.db.insert("answers",{"Question" : 1,"Survey" : 1,"Person" : 2,"Result" : "4"})
        self.assertEqual(len(self.db.retrieve("answers")),1)

    def test_insert_nonexistent_column(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.db.insert("answers",{"Question" : 1,"Person" : 2,"Result" : "4","Total" : 32})
        
    def test_insert_nonexistent_table(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.db.insert("test",{"Question" : 1,"Person" : 2,"Result" : "4","Total" : 32})

    def test_insert_incorrect_type(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.db.insert("answers",{"Question" : "ed", "Person" : 2,"Result" : "4","Total" : 32})

    #Retrieve Test
    def test_retrieve_users_one(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieve("users",{"Name" : "testuc" })),1)

    def test_retrieve_users_all(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieve("users")),3)

    def test_retrieve_tutorials_one(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieve("tutorials",{"unit" : "CAB201" })),1)

    def test_retrieve_tutorials_all(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieve("tutorials")),2)
    
    def test_retrieve_questions_one(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieve("questions",{"ID" : 1 })),1)

    def test_retrieve_questions_all(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieve("questions")),2)

    def test_retrieve_survey_one(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieve("surveys",{"tutorial" : "TUE - 10AM - GP-P504" })),1)

    def test_retrieve_survey_all(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieve("surveys")),2)

    def test_retrieve_answers_one(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieve("answers",{"Question" : 1 })),1)

    def test_retrieve_answers_all(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieve("answers")),2)

    def test_retrieve_no_match(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieve("answers",{"Person" : 1})),0)

    def test_retrieve_mulit_where(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieve("tutorials",{"tutor" : 1, "unit" : "CAB202"})),1)

    def test_retrieve_nonexistent_column(self):
        self.loadTestData()
        with self.assertRaises(sqlite3.OperationalError):
            self.db.retrieve("tutorials",{"tutor" : 1, "result" : "CAB202"})
        
    def test_retrieve_nonexistent_column(self):
        self.loadTestData()
        with self.assertRaises(sqlite3.OperationalError):
            self.db.retrieve("tests",{"tutor" : 1, "result" : "CAB202"})

    def test_retrieve_incorrect_type(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieve("answers",{"Question" : "ed"})),0)
    
    #Retrieve Query Test
    def test_retrieveQuery_one(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieveQuery("* FROM users WHERE Name = 'testuc'" )),1)

    def test_retrieveQuery_all(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieveQuery("* FROM users")),3)

    def test_retrieveQuery_certain_fields(self):
        self.loadTestData()
        result = self.db.retrieveQuery("ID, Tutorial FROM surveys") 
        self.assertEqual(len(result),2)
        self.assertEqual(list(result[0].keys()).sort(),["ID","Tutorial"].sort())

    def test_retrieveQuery_no_match(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieveQuery("* FROM answers WHERE Person = 1")),0)

    def test_retrieveQuery_mulit_where(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieveQuery("* FROM tutorials WHERE tutor = 1 AND unit = 'CAB202'")),1)

    def test_retrieveQuery_join(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieveQuery("tutorials.ID, tutorials.Tutor, users.Email FROM tutorials INNER JOIN users ON tutorials.Tutor = users.ID")),2)

    def test_retrieveQuery_3table_join(self):
        self.loadTestData()
        self.assertEqual(len(self.db.retrieveQuery("tutorials.Tutor, surveys.Tutorial, users.Email FROM ((tutorials INNER JOIN users ON tutorials.Tutor = users.ID) INNER JOIN surveys ON tutorials.ID = surveys.Tutorial)")),2)
    
    def test_retrieveQuery_nonexistent_column(self):
        self.loadTestData()
        with self.assertRaises(sqlite3.OperationalError):
            self.db.retrieveQuery("* FROM tutorials WHERE tutor = 1 AND result = CAB202")
        
    def test_retrieveQuery_nonexistent_column(self):
        self.loadTestData()
        with self.assertRaises(sqlite3.OperationalError):
            self.db.retrieveQuery("* FROM tests WHERE tutor = 1 AND result = CAB202")

    def test_retrieveQuery_incorrect_type(self):
        self.loadTestData()
        with self.assertRaises(sqlite3.OperationalError):
            self.db.retrieveQuery("* FROM answers WHERE Question = ed")

    #Update test
    def test_update_users(self):
        self.loadTestData()
        origEntry = self.db.retrieve("users",{"Name" : "testuc"})[0]
        entry = self.db.retrieve("users",{"Name" : "testuc"})[0]  
        entry["Email"] = "newemail@qut.edu.au"
        self.db.update("users",entry,("ID",entry["ID"]))
        results = self.db.retrieve("users",{"Name" : "testuc"})
        newEntry = results[0]
        self.assertNotEqual(origEntry["Email"],newEntry["Email"])

    def test_update_tutorials(self):
        self.loadTestData()
        origEntry = self.db.retrieve("tutorials",{"ID" : "MON - 2PM - GP-S504"})[0]
        entry = self.db.retrieve("tutorials",{"ID" : "MON - 2PM - GP-S504"})[0]
        entry["Tutor"] = 1
        self.db.update("tutorials",entry,("ID",entry["ID"]))
        results = self.db.retrieve("tutorials",{"ID" : "MON - 2PM - GP-S504"})
        newEntry = results[0]
        self.assertNotEqual(origEntry["Tutor"],newEntry["Tutor"])
    
    def test_update_questions(self):
        self.loadTestData()
        origEntry = self.db.retrieve("questions",{"ID" : 1})[0]
        entry = self.db.retrieve("questions",{"ID" : 1})[0]        
        entry["Answer_text"] = "6-10"
        self.db.update("questions",entry,("ID",entry["ID"]))
        results = self.db.retrieve("questions",{"ID" : 1})
        newEntry = results[0]
        self.assertNotEqual(origEntry["Answer_text"],newEntry["Answer_text"])
    
    def test_update_surveys(self):
        self.loadTestData()
        origEntry = self.db.retrieve("surveys",{"Tutorial" : "MON - 2PM - GP-S504"})[0]
        entry = self.db.retrieve("surveys",{"Tutorial" : "MON - 2PM - GP-S504"})[0] 
        entry["Date"] = "19/06/17"
        self.db.update("surveys",entry,("ID",entry["ID"]))
        results = self.db.retrieve("surveys",{"Tutorial" : "MON - 2PM - GP-S504"})
        newEntry = results[0]
        self.assertNotEqual(origEntry["Date"],newEntry["Date"])
    
    def test_update_answers(self):
        self.loadTestData()
        origEntry = self.db.retrieve("answers",{"Question" : 1})[0]
        entry = self.db.retrieve("answers",{"Question" : 1})[0]
        entry["Result"] = 1
        self.db.update("answers",entry,("ID",entry["ID"]))
        results = self.db.retrieve("answers",{"Question" : 1})
        newEntry = results[0]
        self.assertNotEqual(origEntry["Result"],newEntry["Result"])

    def test_update_nonexistent_column(self):
        self.loadTestData()
        with self.assertRaises(sqlite3.OperationalError):
            self.db.update("answers",{"Question" : 1,"Person" : 2,"Result" : "4","Total" : 32},("Question",1))
        
    def test_update_nonexistent_table(self):
        self.loadTestData()
        with self.assertRaises(sqlite3.OperationalError):
            self.db.update("test",{"Question" : 1,"Person" : 2,"Result" : "4","Total" : 32},("Question",1))

    def test_update_incorrect_type(self):
        self.loadTestData()
        with self.assertRaises(sqlite3.OperationalError):
            self.db.update("answers",{"Question" : "ed", "Person" : 2,"Result" : "4","Total" : 32},("ID",1))
    
    def test_update_conflicting_unique (self):
        self.loadTestData()
        with self.assertRaises(sqlite3.OperationalError):
            self.db.update("answers",{"ID" : "2", "Question" : "ed", "Person" : 2,"Result" : "4","Total" : 32},("ID",1))

    #Delete test
    def test_detete_users(self):
        self.loadTestData()
        self.db.delete("users","Name","testuser")
        self.assertEqual(len(self.db.retrieve("users",{"Name" : "testuser"})),0)

    def test_delete_tutorials(self):
        self.loadTestData()
        self.db.delete("tutorials","id","MON - 2PM - GP-S504")
        self.assertEqual(len(self.db.retrieve("tutorials",{"id":"MON - 2PM - GP-S504"})),0)
    
    def test_delete_questions(self):
        self.loadTestData()
        self.db.delete("questions","ID",1) 
        self.assertEqual(len(self.db.retrieve("questions",{"ID" : 1})),0)
    
    def test_delete_surveys(self):
        self.loadTestData()
        self.db.delete("surveys","Tutorial","MON - 2PM - GP-S504")
        self.assertEqual(len(self.db.retrieve("surveys",{"Tutorial" : "MON - 2PM - GP-S504"})),0)
    
    def test_delete_answers(self):
        self.loadTestData()
        self.db.delete("answers","Question",1)
        self.assertEqual(len(self.db.retrieve("answers",{"Question" : 1})),0)

    def test_delete_nonexistent_column(self):
        self.loadTestData()
        with self.assertRaises(sqlite3.OperationalError):
            self.db.delete("answers","Total",32)
        
    def test_delete_nonexistent_table(self):
        self.loadTestData()
        with self.assertRaises(sqlite3.OperationalError):
            self.db.delete("test","Question",1)

    def test_delete_incorrect_type(self):
        self.loadTestData()
        self.db.delete("answers","Question","ed")
        self.assertEqual(len(self.db.retrieve("answers")),2)

if __name__ == '__main__':
    filen = "Test.db"
    try:
        os.remove(filen)
    except:
        pass
    unittest.main()



