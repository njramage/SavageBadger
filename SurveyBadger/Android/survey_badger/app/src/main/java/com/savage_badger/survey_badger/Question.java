package com.savage_badger.survey_badger;

import java.util.List;
import android.graphics.Bitmap;
import android.support.v4.app.Fragment;

/**
 * Created by nathan on 14/12/16.
 */

public class Question  {

    private int id;
    private String question;
    private String type;
    private List<String> answers;
    private List<Bitmap> images;

    // Used to create a question object
    public Question(int id, String question, String type, List<String> answers) {
        this.id = id;
        this.question = question;
        this.type = type;
        this.answers = answers;
    }

    /* Getters and Setters */

    public void setId(int id)
    {
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public String getQuestion() {
        return question;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getType() {
        return type;
    }

    public void setAnswers(List<String> answers) {
        this.answers = answers;
    }

    public List<String> getAnswers() {
        return answers;
    }
    
    public void setImages(List<Bitmap> images) {
        this.images = images;
    }

    public List<Bitmap> getImages() {
        return this.images;
    }
}
