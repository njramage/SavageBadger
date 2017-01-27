package com.savage_badger.survey_badger;

import android.os.AsyncTask;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.NumberPicker;
import android.widget.RelativeLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.ListIterator;

import HTTPCom.httpCom;

public class MainActivity extends AppCompatActivity {

    private JSONObject jsonObject;
    private ArrayList<Question> questionsList;
    private ArrayList<Answer> answersList;
    private int currentQuestion;
    private boolean optionPicked;
    private int person_id = 1;// defualt player id for testing
    private String token = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        currentQuestion = 1;// Start at first question

        fetchTask getQuestions = new fetchTask();
        getQuestions.execute("Transpotation_Survey");
    }

    // gets survey questions as a JSON object
    public void getSurvey(JSONObject s) {
        // reset questions and answers
        questionsList = new ArrayList<Question>();

        answersList = new ArrayList<Answer>();

        try {
            this.token = s.getString("token");
            createQuestions(s);/// convert JSON object into a list of question objects
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
    public void displayQuestions(ArrayList<Question> questions) {
        int i = 0;// the current question index

        // find the type of question
        while (i < questions.size()) {
            optionPicked = false;
            // if the question is a selection question
            if (questions.get(i).getType() == getResources().getString(R.string.question_selection)) {
                selectionQuestion(questions.get(i));
            }
            // if the question is a number question
            else if (questions.get(i).getType() == getResources().getString(R.string.question_number)) {
                numberQuestion(questions.get(i));
            }
            // if the question is a money question
            else if (questions.get(i).getType() == getResources().getString(R.string.question_money)) {
                //TODO: question_money display, OJ
            }
            // if the question is a set time question
            else if (questions.get(i).getType() == getResources().getString(R.string.question_set_time)) {
                //TODO: question_set_time display Nathan
            }
            // if the question is a time duration question
            else if (questions.get(i).getType() == getResources().getString(R.string.question_time_duration)) {
                numberQuestion(questions.get(i));
            }
        }
    }

    public void selectionQuestion(Question question) {
        setContentView(R.layout.selection_question);
        //TODO: OJ to finish
        TextView question_text = (TextView) findViewById(R.id.title_selection_question);
        question_text.setText(question.getQuestion());

        Button selectedQuestion = (Button) findViewById(R.id.Option1);
        /*RelativeLayout.LayoutParams btnParams = (RelativeLayout.LayoutParams) selectedQuestion.getLayoutParams();
        btnParams.addRule((RelativeLayout.ALIGN_START));
        selectedQuestion.setLayoutParams(btnParams);*/
        final Button button = (Button) findViewById(R.id.Option2);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                // Use onClick to save answer and move onto the next question
                
                //https://developer.android.com/reference/android/widget/Button.html
                //https://developer.android.com/training/basics/firstapp/starting-activity.html
                //http://stackoverflow.com/questions/20156733/how-to-add-button-click-event-in-android-studio
                //http://stackoverflow.com/questions/32469674/how-to-create-two-android-button-using-android-studio
            }
        });


    }

    // display for number question
    public void numberQuestion(Question question){
        setContentView(R.layout.number_question);

        // display the question
        TextView question_text = (TextView) findViewById(R.id.title_number_question);
        question_text.setText(question.getQuestion());

        NumberPicker selectedNumber = (NumberPicker) findViewById(R.id.number_pick);

        selectedNumber.setMinValue(1);
        selectedNumber.setMaxValue(Integer.parseInt(question.getAnswers().get(0)));// get max value from the question object

        while (!optionPicked) {}; // pause while the user hasn't picked an option

        saveAnswer(question.getId(), person_id, Integer.toString(selectedNumber.getValue()));
    }

    // onClick method for a number question
    public void pickNumber(View view) {
        optionPicked = true;
    }

    // create a new answer and add it to the end of the answers list
    public void saveAnswer(int question, int person, String result){
        Answer answer = new Answer(question, person, result);
        answersList.add(answer);
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
