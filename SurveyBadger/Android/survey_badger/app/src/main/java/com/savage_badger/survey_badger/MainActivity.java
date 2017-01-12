package com.savage_badger.survey_badger;

import android.os.AsyncTask;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

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
    private List<Question> questionsList;
    private List<Answer> answersList;
    private int currentQuestion;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        currentQuestion = 1;// Start at first question
    }

    // gets survey questions as a JSON object
    public void getSurvey() {
        // reset questions and answers
        questionsList = new ArrayList<Question>();

        answersList = new ArrayList<Answer>();

        jsonObject = null;
        createQuestions(jsonObject);/// convert JSON object into a list of question objects
    }

    // Creates a list of question objects
    public void createQuestions(JSONObject jsonObject) {

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
    public JSONArray sendAnswers(ArrayList<Answer> answersList) {
        return new JSONArray(answersList);
    }

    //Server connection tasks
    private class fetchTask extends AsyncTask<Integer, JSONObject, JSONObject> {

        @Override
        protected void onPreExecute() {
            //Update GUI before execute
        }

        @Override
        protected JSONObject doInBackground(Integer... params) {
            JSONObject res = null;
            res = httpCom.getSurvey(params[0]);
            return res;
        }

        @Override
        protected void onPostExecute(JSONObject s) { createQuestions(s); }
    }

}
