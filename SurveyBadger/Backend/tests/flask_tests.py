#!/usr/bin/env python

import os
import sys
from shutil import copyfile
import unittest
import tempfile
import json
import time
import re
import subprocess

#Change to src directory for testing and importing
sys.path.append(os.path.abspath('..'))

import views
#from db import Database
from load_testDB import setupDatabase, getDatabase

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.filen = "Polavo.db"
        copyfile("Test_base.db",self.filen)
        views.app.config['TESTING'] = True
        views.app.config['SECRET_KEY'] = "thisisaupersecretkeysuchsecure"
        self.app = views.app.test_client()

    def tearDown(self):
        self.logout()

    def getJsonResult(self,rv):
        return json.loads(rv.data.decode('UTF-8'))


    def login(self, username, password):
        return self.getJsonResult(self.app.post('/login',data=json.dumps(dict(
            username=username,
            password=password)),
            content_type='application/json', 
            follow_redirects=True))

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    #Login tests
    def test_login_student(self):
        rv = self.login('n0000001','wordpass')
        assert 'status' in rv
        assert rv['status'] == True
        rv = self.logout()
        assert b'Welcome' in rv.data
        assert b'>Logout<' not in rv.data

    def test_login_tutor(self):
        rv = self.login('tutorOne','wordpass')
        assert 'status' in rv
        assert rv['status'] == True
        rv = self.logout()
        assert b'Welcome' in rv.data
        assert b'>Logout<' not in rv.data
    
    def test_login_uc(self):
        rv = self.login('ucOne','wordpass')
        assert 'status' in rv
        assert rv['status'] == True
        rv = self.logout()
        assert b'Welcome' in rv.data
        assert b'>Logout<' not in rv.data
    
    def test_login_bad_password(self):
        rv = self.login('ucOne','password')
        assert 'status' in rv
        assert rv['status'] == False
    
    def test_login_bad_password(self):
        rv = self.login('n1111111','wordpass')
        assert 'status' in rv
        assert rv['status'] == False
     
    #Getoptions tests
    def test_getOptions_no_login(self):
        with self.app as c:
            rv = self.app.get('/', follow_redirects=True)
            assert rv.status_code == 200
            assert b'Login' in rv.data
            opts = views.getOptions()
            assert 'LoggedIn' in opts
            assert opts['LoggedIn'] == False
        
    def test_getOptions_studentLogin(self):
        with self.app as c:
            rv = self.login('n0000001','wordpass')
            rv = self.app.get('/', follow_redirects=True)
            assert rv.status_code == 200
            assert b'Please wait' in rv.data
            opts = views.getOptions()
            assert 'LoggedIn' in opts
            assert 'UC' in opts
            assert opts['LoggedIn'] == True
            assert opts['UC'] == False

    def test_getOptions_tutorLogin(self):
        with self.app as c:
            rv = self.login('tutorOne','wordpass')
            rv = self.app.get('/', follow_redirects=True)
            assert rv.status_code == 200
            assert b'Select Your Tutorial' in rv.data
            opts = views.getOptions()
            assert 'LoggedIn' in opts
            assert 'UC' in opts
            assert opts['LoggedIn'] == True
            assert opts['UC'] == False
    
    def test_getOptions_UCLogin(self):
        with self.app as c:
            rv = self.login('ucOne','wordpass')
            #assert rv['status'] == True
            rv = self.app.get('/', follow_redirects=True)
            assert rv.status_code == 200
            assert b'Switch Mode' in rv.data
            opts = views.getOptions()
            assert 'LoggedIn' in opts
            assert 'UC' in opts
            assert opts['LoggedIn'] == True
            assert opts['UC'] == True
    
    #Index tests
    def test_home_no_login(self):
        rv = self.app.get('/', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Login' in rv.data
    
    def test_home_student(self):
        rv = self.login('n0000001','wordpass')
        rv = self.app.get('/', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Please wait' in rv.data
    
    def test_home_tutor(self):
        rv = self.login('tutorOne','wordpass')
        rv = self.app.get('/', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Select Your Tutorial' in rv.data
    
    def test_home_uc(self):
        rv = self.login('ucOne','wordpass')
        rv = self.app.get('/', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Weekly Overview' in rv.data
    
    #Survey tests
    def test_survey_no_login(self):
        rv = self.app.get('/survey', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Login' in rv.data

    def test_survey_student(self):
        rv = self.login('n0000001','wordpass')
        rv = self.app.get('/survey', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Please wait' in rv.data
    
    def test_survey_tutor(self):
        rv = self.login('tutorOne','wordpass')
        rv = self.app.get('/survey', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Select Your Tutorial' in rv.data
    
    def test_survey_UC(self):
        rv = self.login('ucOne','wordpass')
        rv = self.app.get('/survey', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Weekly Overview' in rv.data
        
    #Tutor tests
    def test_tutor_no_login(self):
        rv = self.app.get('/tutor', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Login' in rv.data

    def test_tutor_student(self):
        rv = self.login('n0000001','wordpass')
        rv = self.app.get('/tutor', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Please wait' in rv.data
    
    def test_tutor_tutor(self):
        rv = self.login('tutorOne','wordpass')
        rv = self.app.get('/tutor', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Select Your Tutorial' in rv.data
    
    def test_tutor_UC(self):
        rv = self.login('ucOne','wordpass')
        rv = self.app.get('/tutor', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Select Your Tutorial' in rv.data

    #Dashboard tests
    def test_dashboard_no_login(self):
        rv = self.app.get('/dashboard', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Login' in rv.data

    def test_dashboard_student(self):
        rv = self.login('n0000001','wordpass')
        rv = self.app.get('/dashboard', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Please wait' in rv.data
    
    def test_dashboard_tutor(self):
        rv = self.login('tutorOne','wordpass')
        rv = self.app.get('/dashboard', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Select Your Tutorial' in rv.data
    
    def test_dashboard_UC(self):
        rv = self.login('ucOne','wordpass')
        rv = self.app.get('/dashboard', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Weekly Overview' in rv.data

    #Unit Editor tests
    def test_unitEditor_no_login(self):
        rv = self.app.get('/uniteditor', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Login' in rv.data

    def test_unitEditor_student(self):
        rv = self.login('n0000001','wordpass')
        rv = self.app.get('/uniteditor', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Please wait' in rv.data
    
    def test_unitEditor_tutor(self):
        rv = self.login('tutorOne','wordpass')
        rv = self.app.get('/uniteditor', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Select Your Tutorial' in rv.data
    
    def test_unitEditor_UC(self):
        rv = self.login('ucOne','wordpass')
        rv = self.app.get('/uniteditor', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Please wait' in rv.data
    
    #Unit Editor tests
    def test_unitEditor_no_login(self):
        rv = self.app.get('/uniteditor', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Login' in rv.data

    def test_unitEditor_student(self):
        rv = self.login('n0000001','wordpass')
        rv = self.app.get('/uniteditor', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Please wait' in rv.data
    
    def test_unitEditor_tutor(self):
        rv = self.login('tutorOne','wordpass')
        rv = self.app.get('/uniteditor', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Select Your Tutorial' in rv.data
    
    def test_unitEditor_UC(self):
        rv = self.login('ucOne','wordpass')
        rv = self.app.get('/uniteditor', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Please wait' in rv.data
    
    #Get Survey tests
    def test_getSurvey_no_login(self):
        rv = self.app.get('/getsurvey/DEF456', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Login' in rv.data

    def test_getSurvey_student(self):
        rv = self.login('n0000001','wordpass')
        rv = self.app.get('/getsurvey/DEF456', follow_redirects=True)
        res = self.getJsonResult(rv)
        assert rv.status_code == 200
        assert 'status' in res
        assert 'survey' in res
        assert 'questions' in res
        assert res['status'] == True
        assert len(res['questions']) == 5
    
    def test_getSurvey_tutor(self):
        rv = self.login('tutorOne','wordpass')
        rv = self.app.get('/getsurvey/DEF456', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Select Your Tutorial' in rv.data
    
    def test_getSurvey_UC(self):
        rv = self.login('ucOne','wordpass')
        rv = self.app.get('/getsurvey/DEF456', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Weekly Overview' in rv.data
    
    #Submit Survey tests
    def test_submitSurvey_no_login(self):
        results = [{"Question" : 1,"Result" : "4"},
                {"Question" : 2,"Result" : "3"},
                {"Question" : 3,"Result" : "3"},
                {"Question" : 4,"Result" : "3"},
                {"Question" : 5,"Result" : "4"}]
        
        rv = self.app.post('/submitsurvey',data=json.dumps(dict(
            survey=2,
            answers=results)),
            content_type='application/json', 
            follow_redirects=True)
        
        assert rv.status_code == 200
        assert b'Login' in rv.data

    def test_submitSurvey_student(self):
        results = [{"Question" : 1,"Result" : "4"},
                {"Question" : 2,"Result" : "3"},
                {"Question" : 3,"Result" : "3"},
                {"Question" : 4,"Result" : "3"},
                {"Question" : 5,"Result" : "4"}]
        
        login = self.login('n0000001','wordpass')
        rv = self.app.post('/submitsurvey/',data=json.dumps(dict(
            survey=2,
            answers=results)),
            content_type='application/json', 
            follow_redirects=True)
        
        assert rv.status_code == 200
        res = self.getJsonResult(rv)
        assert 'status' in res
        assert res['status'] == True

    def test_submitSurvey_tutor(self):
        results = [{"Question" : 1,"Result" : "4"},
                {"Question" : 2,"Result" : "3"},
                {"Question" : 3,"Result" : "3"},
                {"Question" : 4,"Result" : "3"},
                {"Question" : 5,"Result" : "4"}]
        
        rv = self.login('tutorOne','wordpass')
        rv = self.app.post('/submitsurvey',data=json.dumps(dict(
            survey=2,
            answers=results)),
            content_type='application/json', 
            follow_redirects=True)
      
        assert rv.status_code == 200
        assert b'Select Your Tutorial' in rv.data
    
    def test_submitSurvey_UC(self):
        results = [{"Question" : 1,"Result" : "4"},
                {"Question" : 2,"Result" : "3"},
                {"Question" : 3,"Result" : "3"},
                {"Question" : 4,"Result" : "3"},
                {"Question" : 5,"Result" : "4"}]
        
        rv = self.login('ucOne','wordpass')
        
        rv = self.app.post('/submitsurvey',data=json.dumps(dict(
            survey=2,
            answers=results)),
            content_type='application/json', 
            follow_redirects=True)
        
        assert rv.status_code == 200
        assert b'Weekly Overview' in rv.data

if __name__ == '__main__':
    #Load database
    filen = "Test_base.db"
    redisStore = "dump.rdb"
    try:
        os.remove(filen)
        os.remove(redisStore)
    except:
        pass
    setupDatabase(filen)
    #Check if redis server is running
    redis = False
    s = subprocess.Popen(["ps", "e"],stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(b'redis-server', x):
            redis = True

    if not redis:
        opt = input("Redis-server is not running. Would you like to run it now?[y/n] ")
        if opt.lower() == "y":
            #Start redis
            os.system('redis-server &') 
            #Sleep to let redis start
            #time.sleep(2)
        else:
            print("Aborting")
            sys.exit()
    #Run tests
    unittest.main()
    
