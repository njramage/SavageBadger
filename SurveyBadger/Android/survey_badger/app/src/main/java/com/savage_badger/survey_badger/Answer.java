package com.savage_badger.survey_badger;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by nathan on 14/12/16.
 */

public class Answer {

    private int questionID;
    private String result;

    // Used to create an Answer object
    public Answer() {
        questionID = 0;
        result = "No result";
    }

    public Answer(int questionID, String result) {
        this.questionID = questionID;;
        this.result = result;
    }

    /* Getters and Setters */

    public void setQuestionID(int id) {
        questionID = id;
    }

    public int getQuestionID() {
        return questionID;
    }

    public void setResult(String answer) {
        result = answer;
    }

    public String getResult() {
        return result;
    }

    //Returns a JSONObject used for sending to the server
    public JSONObject toJson() {
        JSONObject answerJSON = new JSONObject();
        try {
            answerJSON.put("Question", questionID);
            answerJSON.put("Result", result);
            return answerJSON;
        } catch (JSONException e) {
            e.printStackTrace();
            return null;
        }
    }
}
