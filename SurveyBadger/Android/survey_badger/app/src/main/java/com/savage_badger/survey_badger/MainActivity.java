package com.savage_badger.survey_badger;

import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.NumberPicker;
import android.widget.TextView;
import android.widget.TimePicker;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";
    private static final String QUESTION_FRAGMENT = "QUESTION_FRAGMENT";

    private JSONObject jsonObject;
    private ArrayList<Question> questionsList;
    private ArrayList<Answer> answersList;
    private int currentQuestion;
    private int person_id = 1;// defualt value for testing
    private String token = null;
    private String survey;
    private View main_Activity_View, number_Question_View, selection_Question_View, login_view;
    private TextView Question_Title;

    /*
    * Login varibles
    */
    private Button login_btn;
    private EditText username, password;
    private int counter = 10;
    private Map<String, Boolean> map;// holds result from server

    /*
     * Code Check variables
     */
    private EditText entered_code;

    private List<Image> bitmapImages;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        login_view = getLayoutInflater().inflate(R.layout.fragment_login, null);
        main_Activity_View = getLayoutInflater().inflate(R.layout.activity_main, null);
        number_Question_View = getLayoutInflater().inflate(R.layout.number_question, null);
        selection_Question_View = getLayoutInflater().inflate(R.layout.number_question, null);

        setContentView(main_Activity_View);

        answersList = new ArrayList<Answer>();

        currentQuestion = 0;// Start at first question

        getSupportActionBar().setDisplayOptions(ActionBar.DISPLAY_SHOW_CUSTOM);
        getSupportActionBar().setCustomView(R.layout.abs_layout);

        map = new HashMap<String, Boolean>();

        displayLogin();
    }

    /*
     * Name: displayLogin
     * Description: Displays the login fragment
     * Input: None
     * Output: None
     */
    public  void displayLogin() {
        FragmentManager fm = getSupportFragmentManager();
        FragmentTransaction ft = fm.beginTransaction();

        // Create a new instance of a login fragment
        LoginFragment loginFrag = new LoginFragment();
        ft.add(R.id.fragment_container, loginFrag, QUESTION_FRAGMENT);
        ft.commit();
    }// End displayLogin()

    /*
     * Name: displayCodeCheck
     * Description: Displays the code check fragment
     * Input: None
     * Output: None
     */
    public  void displayCodeCheck() {
        FragmentManager fm = getSupportFragmentManager();
        Fragment fragment = fm.findFragmentByTag(QUESTION_FRAGMENT);// find any active fragments with the QUESTION_FRAGMENT tag
        FragmentTransaction ft = fm.beginTransaction();

        // Create a new instance of a login fragment
        CodeFragment codefrag = new CodeFragment();

        // if there are is an active fragment, replace the old fragment with the new one and commit
        if (fragment != null) {
            ft.replace(R.id.fragment_container, codefrag, QUESTION_FRAGMENT);
            ft.commit();
        }
        else {// add the new framgent and commit
            ft.add(R.id.fragment_container, codefrag, QUESTION_FRAGMENT);
            ft.commit();
        }

    }// End displayCodeCheck()

    // create jsonArray to send answer back
    public void sendAnswers(ArrayList<Answer> answersList) {
        JSONObject data = new JSONObject();
        try {
            data.put("token",this.token);

            //Put all answers into a JSONArray to send to server
            JSONArray answers = new JSONArray();
            for (Answer ans:answersList) {
                answers.put(ans.toJson());
            }
            data.put("answers", answers);

            SendTask sendAnswers = new SendTask();
            sendAnswers.execute(data);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    // display questions
    public void displayQuestions(final ArrayList<Question> questions) {
        Log.i ("in displayQuestions", "test");

        FragmentManager fm = getSupportFragmentManager();
        Fragment fragment = fm.findFragmentByTag(QUESTION_FRAGMENT);// find any active fragments with the QUESTION_FRAGMENT tag
        FragmentTransaction ft = fm.beginTransaction();// begin a fragment transcation

        if (currentQuestion < questions.size())
        {

            // if the question is a selection question
            if (questions.get(currentQuestion).getType().equals(getString(R.string.question_selection))) {
                Log.i ("getting into Select", "testing");
                SelectionFragment selectionFragment = SelectionFragment.newInstance(questions.get(currentQuestion));
                if (fragment != null)
                {
                    ft.replace(R.id.fragment_container, selectionFragment, QUESTION_FRAGMENT);
                    ft.commit();
                }
                else
                {
                 ft.add(R.id.fragment_container, selectionFragment, QUESTION_FRAGMENT);
                    ft.commit();
                }


                bitmapImages = questions.get(currentQuestion).getImages();

            }


            // if the question is a number question
            else if (questions.get(currentQuestion).getType().equals(getString(R.string.question_number))) {
                // create a new instance of a Number Fragment
                NumberFragment numberFragment = NumberFragment.newInstance(questions.get(currentQuestion));

                // if there are is an active fragment, replace the old fragment with the new one and commit
                if (fragment != null) {
                    ft.replace(R.id.fragment_container, numberFragment, QUESTION_FRAGMENT);
                    ft.commit();
                }
                else {// add the new framgent and commit
                    ft.add(R.id.fragment_container, numberFragment, QUESTION_FRAGMENT);
                    ft.commit();
                }
            }
            // if the question is a money question
            else if (questions.get(currentQuestion).getType().equals(getString(R.string.question_money))) {
                // create a new instance of a Number Fragment
                NumberFragment numberFragment = NumberFragment.newInstance(questions.get(currentQuestion));

                // if there are is an active fragment, replace the old fragment with the new one and commit
                if (fragment != null) {
                    ft.replace(R.id.fragment_container, numberFragment, QUESTION_FRAGMENT);
                    ft.commit();
                }
                else {// add the new framgent and commit
                    ft.add(R.id.fragment_container, numberFragment, QUESTION_FRAGMENT);
                    ft.commit();
                }
            }
            // if the question is a set time question
            else if (questions.get(currentQuestion).getType().equals(getString(R.string.question_set_time))) {
                // create a new instance of a Number Fragment
                TimeFragment timeFragment = TimeFragment.newInstance(questions.get(currentQuestion));

                // if there are is an active fragment, replace the old fragment with the new one and commit
                if (fragment != null) {
                    ft.replace(R.id.fragment_container, timeFragment, QUESTION_FRAGMENT);
                    ft.commit();
                }
                else {// add the new framgent and commit
                    ft.add(R.id.fragment_container, timeFragment, QUESTION_FRAGMENT);
                    ft.commit();
                }
            }
            // if the question is a time duration question
            else if (questions.get(currentQuestion).getType().equals(getString(R.string.question_time_duration))) {
                // create a new instance of a Number Fragment
                NumberFragment numberFragment = NumberFragment.newInstance(questions.get(currentQuestion));

                // if there are is an active fragment, replace the old fragment with the new one and commit
                if (fragment != null) {
                    ft.replace(R.id.fragment_container, numberFragment, QUESTION_FRAGMENT);
                    ft.commit();
                }
                else {// add the new framgent and commit
                    ft.add(R.id.fragment_container, numberFragment, QUESTION_FRAGMENT);
                    ft.commit();
                }
            }
        }
        else { /// end of survey show confirmation screen
            Log.d("Main Activity", "Finished Survey");
            if (fragment != null) {
                sendAnswers(answersList);
                FinishedSurveyFragment finisedFragment = new FinishedSurveyFragment();
                ft.replace(R.id.fragment_container, finisedFragment, QUESTION_FRAGMENT);
                ft.commit();
            }
        }
    }

    /*
     * Description: Checks the code entered by the user is a vaild survey code
     * Input: The the layout layout as a view
     * Output: None
     */
    public void code_continue(View view) {
        fetchTask getQuestions = new fetchTask();

        entered_code = (EditText) findViewById(R.id.code_check);

        this.survey = entered_code.getText().toString();
        getQuestions.execute(this.survey);
    }

    /*
     * Name: Login
     * Description: Login checks the enterd credentials against the user credentials in a database.
     *              If there are correct then the user can login, else the attempts counter is
     *              decremented.  If the coutner reeaches zero then the login button is disabled and
     *              the application exits.
     * Input: The the layout layout as a view
     * Output: None
     */
    public void login(View view) {
        // TODO: 22/06/2017 Add proper login authentication
        username = (EditText) findViewById(R.id.username);
        password = (EditText) findViewById(R.id.password);

        loginTask loginTask = new loginTask();

        try {
            Boolean result = loginTask.execute("http://www.polavo.net/login/", username.getText().toString(), password.getText().toString()).get();
            Log.i(TAG, "Usersname: " + username.getText().toString() + "/");
            Log.i(TAG, "password: " + password.getText().toString() + "/");
            if (result) {
                //correcct password
                Log.i(TAG, "Login correct!");

                int userid = 1;// // TODO: 22/06/2017 Get real user id from database

                person_id = userid;

                login_btn = (Button) findViewById(R.id.login_btn);
                login_btn.setEnabled(false);
                Button cancel_btn = (Button) findViewById(R.id.cancel_btn);
                cancel_btn.setEnabled(false);
                displayCodeCheck();
            } else {
                //wrong password
                counter--;// Decremment login attempt counter

                Log.d(TAG, "Wrong password or usename");

                if (counter == 0) {// No more login attempts allowed
                    login_btn.setEnabled(false);// Desable login button
                    finish();// Call onDestroy()
                }
            }
        } catch (InterruptedException e) {
            Log.e(TAG, "Interrupted: " + e);
        } catch (ExecutionException e) {
            Log.e(TAG, "Execution Expection: " + e);
        }

    }// End login()

    /*
     * Name: Cancel
     * Description: Cleans up activity and closes the app
     * Input: Input: The the login layout as a view
     * Output: None
     */
    public void cancel(View view) {
        finish();// Call onDestroy
    }// End Cancel()

    // onClick method for a number question
    public void pickNumber(View view) {
        // find number picker
        NumberPicker numberPicker = (NumberPicker) findViewById(R.id.number_pick);

        // save the chosen answer
        saveAnswer(questionsList.get(currentQuestion).getId(), person_id, Integer.toString(numberPicker.getValue()));
        Log.d("Main Activity", "Saved answer");

        currentQuestion++;// increment question number reference
        Log.d("Main Activity", "Incremented currentQuestion");

        displayQuestions(questionsList);// display the next question
        Log.d("Main Activity", "Moved to next question");

    }

    public void selectionQuestion (View view)
    {
      //  saveAnswer(questionsList.get(currentQuestion).getId(), person_id, Integer.toString());
        currentQuestion++;
        displayQuestions(questionsList);
        //saveAnswer(questionsList.get(currentQuestion).getId(), person_id, );


    }

    // onClick method for a set time question
    public void pickTime(View view) {
        Log.d("Main Activity", "currentQuestion: " + currentQuestion);
        Log.d("Main Activity", "question id: " + questionsList.get(currentQuestion).getId());
        TimePicker timePicker = (TimePicker) findViewById(R.id.time_picker);
        if (Build.VERSION.SDK_INT >= 23)
        {
            saveAnswer(questionsList.get(currentQuestion).getId(), person_id, Integer.toString(timePicker.getHour()) + ":" + Integer.toString(timePicker.getMinute()));
        }
        else {
            saveAnswer(questionsList.get(currentQuestion).getId(), person_id, Integer.toString(timePicker.getCurrentHour()) + ":" + Integer.toString(timePicker.getCurrentMinute()));
        }

        currentQuestion++;// increment question number reference
        displayQuestions(questionsList);// display the next question
    }

    // onClick method for a survey completion screen
    public void getAnotherSurvey(View view) {
        currentQuestion = 0;// Start at first question

        fetchTask getQuestions = new fetchTask();
        getQuestions.execute("123456");
    }

    // create a new answer and add it to the end of the answers list
    public void saveAnswer(int question, int person, String result){
        Log.i("Main Activity", "question " + question);
        Log.i("Main Activity", "result " + result);
        Answer answer = new Answer(question, person, result);
        answersList.add(answer);
        Log.i("Answer",String.valueOf(question)+":"+String.valueOf(person)+":"+result);
    }
    public List<Image> BitmapImages()
    {
       /// ArrayList questions = new ArrayList<Question>;


        return bitmapImages;
        // questions.get(currentQuestion).getType().equals(

    }



    //Server connection tasks
    private class fetchTask extends AsyncTask<String, ArrayList<Question>, ArrayList<Question>> {

        @Override
        protected void onPreExecute() {
            //Update GUI before execute
        }

        @Override
        protected ArrayList<Question> doInBackground(String... params) {
            QuestionList questionListCreator = new QuestionList();
            ArrayList<Question> questions = new ArrayList<Question>();
            JSONObject s = httpCom.getSurvey(params[0]);
            
            try {
                Log.i(TAG, "in try statement");
                if (s.has("questions")) {

                    //Create question list
                    questionListCreator.createQuestions(s);
                    Log.i("Polavo", "first question: " + questionListCreator.getQustionList().get(0));
                } else {
                    Log.e("Polavo","Error occured getting the survey from the server");
                }
            } catch (Exception e) {
                Log.e("Polavo","Error occured getting the survey from the server");
            }
            return questionListCreator.getQustionList();
        }

        @Override
        protected void onPostExecute(ArrayList<Question> questions) {
            questionsList = questions;
            if (questionsList != null){
                displayQuestions(questionsList);
            }
            else {
                Toast.makeText(MainActivity.this, "Wrong code, try again", Toast.LENGTH_SHORT).show();
            }
        }
    }

    private class loginTask extends AsyncTask<String, Boolean, Boolean> {

        @Override
        protected Boolean doInBackground(String... params) {

            Log.i(TAG, "Login");
            // Send user and pass to be checked by server
              /*
              * Create JSON object
              * Username : <Username entered by user>
              * Password : <Password entered by user>
              */

            try {
                JSONObject loginDetails = new JSONObject();
                loginDetails.put("username", params[1].toString());
                loginDetails.put("password", params[2].toString());

                JSONObject result = httpCom.login(loginDetails);

                //Check the result of the query
                if (result.has("status")) {
                    return result.getBoolean("status");
                } else {
                    return false;
                }
            } catch (JSONException e) {
                Log.e(TAG, "JSON Exception: ", e);
                return false;
            }
        }

        @Override
        protected void onPostExecute(Boolean result){
            Log.i("Polavo","Login result: "+result.toString());
        }

    }

    //Server connection tasks
    private class SendTask extends AsyncTask<JSONObject, JSONObject, JSONObject> {

        @Override
        protected void onPreExecute() {
            //Update GUI before execute
        }

        @Override
        protected JSONObject doInBackground(JSONObject... params) {
            JSONObject res = null;
            res = httpCom.sendAnswers(params[0]);
            return res;
        }

        @Override
        protected void onPostExecute(JSONObject s) {
            try {
                if (s.getBoolean("result") == true) {
                    Log.i("Survey Badger","Successfully Submitted Answers");
                } else {
                    Log.i("Survey Badger","Answers not submitted");
                }
            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("Survey Badger","Error retrieving JSON result");
            }



        }


    }
}
