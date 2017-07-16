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
import android.widget.ListView;
import android.widget.NumberPicker;
import android.widget.SeekBar;
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
    private String token = null;
    private String survey;
    private View main_Activity_View, number_Question_View, selection_Question_View, login_view;
    private TextView Question_Title;
    private ListView listView;

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
        //login_view = getLayoutInflater().inflate(R.layout.fragment_login, null);
        main_Activity_View = getLayoutInflater().inflate(R.layout.activity_main, null);
        number_Question_View = getLayoutInflater().inflate(R.layout.number_question, null);
        selection_Question_View = getLayoutInflater().inflate(R.layout.number_question, null);

        setContentView(main_Activity_View);

        answersList = new ArrayList<Answer>();

        currentQuestion = 0;// Start at first question

        getSupportActionBar().setDisplayOptions(ActionBar.DISPLAY_SHOW_CUSTOM);
        getSupportActionBar().setCustomView(R.layout.abs_layout);

        map = new HashMap<String, Boolean>();

        Bundle bundle = getIntent().getExtras();
        questionsList = bundle.getParcelableArrayList("questions");
        survey = bundle.getString("survey");
        displayQuestions(questionsList);

        //displayLogin();
    }

    // create jsonArray to send answer back
    public void sendAnswers(ArrayList<Answer> answersList) {
        JSONObject data = new JSONObject();
        try {
            data.put("survey",this.survey);

            //Put all answers into a JSONArray to send to server
            JSONArray answers = new JSONArray();
            for (int i = 0; i < answersList.size(); i++) {
                answers.put(answersList.get(i).toJson());
            }
            data.put("answers", answers);

            SendTask sendAnswers = new SendTask();
            sendAnswers.execute(data);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    // overrides the back button to decrement the current question id
    @Override
    public void onBackPressed() {
        Log.d(TAG, "Back pressed");
        if (currentQuestion > 0)
        {
            currentQuestion--;
            FragmentManager fm = getSupportFragmentManager();
            fm.popBackStack();
            Log.d(TAG, "Current question: " + String.valueOf(currentQuestion + 1));
        }
    }


    // pops fragment backstack and decrements the current question id
    public void previousQuestion(View view) {
        Log.d(TAG, "Back pressed");
        if (currentQuestion > 0)
        {
            currentQuestion--;
            FragmentManager fm = getSupportFragmentManager();
            fm.popBackStack();
            Log.d(TAG, "Current question: " + String.valueOf(currentQuestion + 1));
        }
    }

    // display questions
    public void displayQuestions(final ArrayList<Question> questions) {
        Log.i ("in displayQuestions", "test");

        FragmentManager fm = getSupportFragmentManager();
        Fragment fragment = fm.findFragmentByTag(QUESTION_FRAGMENT);// find any active fragments with the QUESTION_FRAGMENT tag
        FragmentTransaction ft = fm.beginTransaction().setTransition(FragmentTransaction.TRANSIT_FRAGMENT_FADE).addToBackStack(null);// begin a fragment transcation

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
                    TextView tv = (TextView) findViewById(R.id.textView2);
                    tv.setText("YOLO");
                }
                else
                {
                 ft.add(R.id.fragment_container, selectionFragment, QUESTION_FRAGMENT);
                    ft.commit();
                }


                //bitmapImages = questions.get(currentQuestion).getImages();

            }

            // if the question is a number question
            /*else if (questions.get(currentQuestion).getType().equals(getString(R.string.question_number))) {
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
            }*/
        }
        else { /// end of survey show confirmation screen
            if (fragment != null) {
                FinishedSurveyFragment finisedFragment = new FinishedSurveyFragment();
                ft.replace(R.id.fragment_container, finisedFragment, QUESTION_FRAGMENT);
                ft.commit();
            }
        }
    }

    // onClick method for a number question
    public void pickNumber(View view) {
        // find number picker
        NumberPicker numberPicker = (NumberPicker) findViewById(R.id.number_pick);

        // save the chosen answer
        saveAnswer(questionsList.get(currentQuestion).getId(), Integer.toString(numberPicker.getValue()));
        Log.d("Main Activity", "Saved answer");

        currentQuestion++;// increment question number reference
        Log.d("Main Activity", "Incremented currentQuestion");

        displayQuestions(questionsList);// display the next question
        Log.d("Main Activity", "Moved to next question");

    }

    public void selectionQuestion (View view)
    {
        SeekBar seekbar = (SeekBar) findViewById(R.id.seekBar);
        int result = seekbar.getProgress() + 1;
        //saveAnswer(questionsList.get(currentQuestion).getId(), person_id, String.valueOf(result));
            //check if result already exists
            if (currentQuestion < 5) {
                new Thread(new CheckIfAnswerExists(questionsList.get(currentQuestion).getId(), String.valueOf(result))).start();
            }
            currentQuestion++;
            displayQuestions(questionsList);
//            FragmentManager fm = getSupportFragmentManager();
//            Fragment fragment = fm.findFragmentByTag(QUESTION_FRAGMENT);// find any active fragments with the QUESTION_FRAGMENT tag
//            FragmentTransaction ft = fm.beginTransaction().setTransition(FragmentTransaction.TRANSIT_FRAGMENT_FADE);
//            Log.d("Main Activity", "Finished Survey");
    }

    // onClick method for a set time question
    public void pickTime(View view) {
        Log.d("Main Activity", "currentQuestion: " + currentQuestion);
        Log.d("Main Activity", "question id: " + questionsList.get(currentQuestion).getId());
        TimePicker timePicker = (TimePicker) findViewById(R.id.time_picker);
        if (Build.VERSION.SDK_INT >= 23)
        {
            saveAnswer(questionsList.get(currentQuestion).getId(), Integer.toString(timePicker.getHour()) + ":" + Integer.toString(timePicker.getMinute()));
        }
        else {
            saveAnswer(questionsList.get(currentQuestion).getId(), Integer.toString(timePicker.getCurrentHour()) + ":" + Integer.toString(timePicker.getCurrentMinute()));
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
    public void saveAnswer(int question, String result){
        Log.i("Main Activity", "question " + question);
        Log.i("Main Activity", "result " + result);
        Answer answer = new Answer(question, result);
        answersList.add(answer);
        Log.i("Answer",String.valueOf(question)+":"+":"+result);
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
            Log.i(TAG, "getting survey with code");
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
            Log.i(TAG, "return statement");
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
                if (s.getBoolean("status") == true) {
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

    class CheckIfAnswerExists implements Runnable {

        int idToCheck;
        String result;
        boolean found;

        CheckIfAnswerExists(int qId, String result){
            this.idToCheck = qId;
            this.result = result;
            found = false;
        }

        @Override
        public void run() {
            for (int i = 0; i < answersList.size(); i++) {
                if (answersList.get(i).getQuestionID() == idToCheck - 1) {
                    answersList.get(i).setResult(result);
                    found = true;
                    Log.i(TAG, "Question " + String.valueOf(answersList.get(i).getQuestionID()));
                    Log.i(TAG, "result " + String.valueOf(answersList.get(i).getResult()));
                }
            }

            if (!found) {
                saveAnswer(idToCheck, result);
            }
        }
    }
}
