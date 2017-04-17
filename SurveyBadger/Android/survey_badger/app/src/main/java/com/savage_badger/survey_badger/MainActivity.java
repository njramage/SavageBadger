package com.savage_badger.survey_badger;

import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.NumberPicker;
import android.widget.TextView;
import android.widget.TimePicker;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

import HTTPCom.httpCom;

public class MainActivity extends AppCompatActivity {

    private static final String QUESTION_FRAGMENT = "QUESTION_FRAGMENT";

    private JSONObject jsonObject;
    private ArrayList<Question> questionsList;
    private ArrayList<Answer> answersList;
    private int currentQuestion;
    private int person_id = 1;// defualt player id for testing
    private String token = null;
    private View main_Activity_View, number_Question_View, selection_Question_View;
    private TextView Question_Title;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        main_Activity_View = getLayoutInflater().inflate(R.layout.activity_main, null);
        number_Question_View = getLayoutInflater().inflate(R.layout.number_question, null);
        selection_Question_View = getLayoutInflater().inflate(R.layout.number_question, null);

        setContentView(main_Activity_View);

        currentQuestion = 0;// Start at first question

        fetchTask getQuestions = new fetchTask();

       //this.survey = "Transpotation_Survey";
        this.survey = "I_Like_Food";
        getQuestions.execute(this.survey);
    }

    // gets survey questions as a JSON object
    public void getSurvey(JSONObject s) {
        // reset questions and answers
        questionsList = new ArrayList<Question>();

        answersList = new ArrayList<Answer>();

        try {
            this.token = s.getString("token");
            createQuestions(s);/// convert JSON object into a list of question objects
            displayQuestions(questionsList);

        } catch (JSONException e) {
            e.printStackTrace();
            //TODO Notify user of connection failure
        }
    }

    // Creates a list of question objects
    public void createQuestions(JSONObject jsonObject) {
        Log.i("Questions",jsonObject.toString());

        try {
            // turns Question JSON object into a JSON array for easy manipulation
            JSONArray questions = jsonObject.getJSONArray("questions");

            // fill questions list
            for (int i = 0; i < questions.length(); i++) { // iterate theough all the questions
                JSONObject q = questions.getJSONObject(i);

                // turns Answers JSON object into a JSON array for easy manipulation
                JSONArray answersJSON = q.getJSONArray("answers");

                if (answersJSON.length() > 1){
                    try {
                        // get all possible answers
                        //JSONArray answers = answersJSON.getJSONArray("answers");

                        // store them in an array for easy use
                        ArrayList<String> possibleAnswers = new ArrayList<String>();

                        // fill possible answers list
                        for (int j = 0; j < answersJSON.length(); j++) {
                            String possibleAnswer = answersJSON.getString(j);
                            possibleAnswers.add(possibleAnswer);
                        }

                        // create an answers object
                        Question question = new Question(q.getInt("id"), q.getString("question"), q.getString("type"), possibleAnswers);

                        questionsList.add(question);// add it to the list

                    } catch (JSONException e) {
                        //TODO: Exception message
                    }
                }
                else {
                    ArrayList<String> possibleAnswers = new ArrayList<String>();
                    possibleAnswers.add(answersJSON.getString(0));
                    Question question = new Question(q.getInt("id"), q.getString("question"), q.getString("type"), possibleAnswers);
                    questionsList.add(question);
                }
            }
        } catch (JSONException e) {
            //TODO: Exception message
        }
    }

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

        if (currentQuestion < questionsList.size())
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
        getQuestions.execute("Transpotation_Survey");
    }

    // create a new answer and add it to the end of the answers list
    public void saveAnswer(int question, int person, String result){
        Answer answer = new Answer(question, person, result);
        answersList.add(answer);
        Log.i("Answer",String.valueOf(question)+":"+String.valueOf(person)+":"+result);
    }

    //Server connection tasks
    private class fetchTask extends AsyncTask<String, JSONObject, JSONObject> {

        @Override
        protected void onPreExecute() {
            //Update GUI before execute
        }

        @Override
        protected JSONObject doInBackground(String... params) {
            JSONObject res = null;
            res = httpCom.getSurvey(params[0]);
            return res;
        }

        @Override
        protected void onPostExecute(JSONObject s) { getSurvey(s); }
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
