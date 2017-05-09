package com.savage_badger.survey_badger;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

/**
 * Created by nrama on 9/05/2017.
 */

public class QuestionList {
    ArrayList<Question> questionList;

    public QuestionList() {
        ArrayList<Question> questionList = new ArrayList<Question>();
    }

    public ArrayList<Question> getQustionList() {
        return questionList;
    }

    public void setQuestionList(ArrayList<Question> questions) {
        questionList = questions;
    }

    // Creates a list of question objects
    public void createQuestions(JSONObject jsonObject) {
        questionList = new ArrayList<Question>();
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

                        questionList.add(question);// add it to the list

                    } catch (JSONException e) {
                        //TODO: Exception message
                    }
                }
                else {
                    ArrayList<String> possibleAnswers = new ArrayList<String>();
                    possibleAnswers.add(answersJSON.getString(0));
                    Question question = new Question(q.getInt("id"), q.getString("question"), q.getString("type"), possibleAnswers);
                    questionList.add(question);
                }
            }
        } catch (JSONException e) {
            //TODO: Exception message
        }
    }
}
