package com.savage_badger.survey_badger;

import java.util.List;

import android.os.Parcel;
import android.os.Parcelable;
import android.support.v4.app.Fragment;

/**
 * Created by nathan on 14/12/16.
 */

public class Question implements Parcelable {

    private int id;
    private String question;
    private String type;
    //private List<String> answers;
    //private List<Image> images;

    // Used to create a question object
    public Question(int id, String question, String type/*List<String> answers*/) {
        this.id = id;
        this.question = question;
        this.type = type;
        //this.answers = answers;
    }

    /* Getters and Setters */

    protected Question(Parcel in) {
        id = in.readInt();
        question = in.readString();
        type = in.readString();
        //answers = in.createStringArrayList();
    }

    public static final Creator<Question> CREATOR = new Creator<Question>() {
        @Override
        public Question createFromParcel(Parcel in) {
            return new Question(in);
        }

        @Override
        public Question[] newArray(int size) {
            return new Question[size];
        }
    };

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

//    public void setAnswers(List<String> answers) {
//        this.answers = answers;
//    }

    /*public List<String> getAnswers() {
        return answers;
    }*/
    
    /*public void setImages(List<Image> images) {


         this.images = images;
    }

    public List<Image> getImages() {
        return this.images;
    }*/

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeInt(id);
        dest.writeString(question);
        dest.writeString(type);
        //dest.writeArray(answers.toArray());
    }
}
