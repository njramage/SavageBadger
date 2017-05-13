package com.savage_badger.survey_badger;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;

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
                //initialize question object
                Question question;
                
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
                        question = new Question(q.getInt("id"), q.getString("question"), q.getString("type"), possibleAnswers);

                    } catch (JSONException e) {
                        //TODO: Exception message
                    }
                }
                else {
                    ArrayList<String> possibleAnswers = new ArrayList<String>();
                    possibleAnswers.add(answersJSON.getString(0));
                    question = new Question(q.getInt("id"), q.getString("question"), q.getString("type"), possibleAnswers);
                }

                //Get images from server or local sources
                question.setImages(getQuestionImages(q.getJSONArray("images")));
                questionList.add(question);// add it to the list 
            }
        } catch (JSONException e) {
            //TODO: Exception message
        }
    }

    //gets all the images required for an image
    private List<Bitmap> getQuestionImages(List<Strings> links) {
        List<Bitmap> images = new ArrayList<Bitmap>();
        
        for (String link: links) {
            Bitmap bitmap;
            //If the reference is to a local resource, grab from drawable folder
            if (link.contains("@drawable/")) {
                //TODO: Handle local resources (Issues with application context)
                //Get resource ID
                //int imageResource = getResources().getIdentifier(link, null, getPackageName());
                //bitmap = BitmapFactory.decodeResource(context.getResources(),getResources().getDrawable(imageResource));
                bitmap = null;
            } else {
                bitmap = httpCom.getImage(link);
            }

            images.append(bitmap);
        }

        return images;
    }
}
