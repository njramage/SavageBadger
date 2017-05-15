package com.savage_badger.survey_badger;

import android.app.Fragment;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;
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
                // store them in an array for easy use
                ArrayList<String> possibleAnswers = new ArrayList<String>();

                if (answersJSON.length() > 1){
                    try {
                        // fill possible answers list
                        for (int j = 0; j < answersJSON.length(); j++) {
                            String possibleAnswer = answersJSON.getString(j);
                            possibleAnswers.add(possibleAnswer);
                        }


                    } catch (JSONException e) {
                        //TODO: Exception message
                    }
                }
                else {
                    possibleAnswers.add(answersJSON.getString(0));
                }
                
                // create an answers object
                question = new Question(q.getInt("id"), q.getString("question"), q.getString("type"), possibleAnswers);

                //Get images from server or local sources 
                JSONArray imagesJSON = q.getJSONArray("images");
                ArrayList<Image> images = new ArrayList<Image>();

                //If images, extract their strings and fetch them from the server
                if (imagesJSON.length() != 0 && !imagesJSON.get(0).equals("")) {
                    ArrayList<String> imageLinks = new ArrayList<String>();
                    
                    try {
                        for (int k = 0; k < imagesJSON.length(); k++) {
                            imageLinks.add(imagesJSON.getString(k));
                        } 

                        images = getQuestionImages(imageLinks);    
                    } catch (JSONException e) {
                        Log.e("Polavo","Error occured getting image links for Question ID: "+String.valueOf(question.getId()));
                    }
                }

                question.setImages(images);

                questionList.add(question);// add it to the list 
            }
        } catch (JSONException e) {
            //TODO: Exception message
        }
    }

    //gets all the images required for an image
    private ArrayList<Image> getQuestionImages(List<String> links) {
        ArrayList<Image> images = new ArrayList<Image>();
        
        for (String link: links) {
            Image img = new Image();
            //If the reference is to a local resource, grab from drawable folder
            if (link.contains("@drawable/")) {
                //TODO: Handle local resources (Issues with application context)
                //Get resource ID
                //int imageResource = getResources().getIdentifier(link, null, getPackageName());
                //bitmap = BitmapFactory.decodeResource(context.getResources(),getResources().getDrawable(imageResource));
                img.setValue(link.replace("@drawable/",""));
            } else {
                img.setBitmap(httpCom.getImage(link));
                img.setValue(link);
            }
            images.add(img);
        }

        return images;
    }
}
