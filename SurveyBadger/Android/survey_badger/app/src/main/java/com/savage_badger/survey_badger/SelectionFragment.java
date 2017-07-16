package com.savage_badger.survey_badger;

import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.support.annotation.IntegerRes;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentManager;
import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.SeekBar;
import android.widget.TextView;

import android.util.Log;

import java.lang.reflect.Field;
import java.util.ArrayList;

/**
 * Created by nathan on 27/01/17.
 */

public class SelectionFragment extends Fragment {

    // Tags to help find the arguements the fragment was initialised with
    private static final String QUESTION_TEXT = "QUESTION_TEXT";
    private static final String QUESTION_ANSWERS = "QUESTION_ANSWERS";
    private static final String QUESTION_ID = "QUESTION_ID";


    private String[] answers;
    private String questionText;
    private int qID;
    private int person_id = 1;// defualt player id for testing
    private SeekBar seekBar;
    private ImageView indicator;

    // array of images
    private String[] satisfaction = {"unhappy", "ok", "neutral", "good", "happy"};

    public SelectionFragment () {

    }

    public static SelectionFragment newInstance(Question question) {

        // Translate answers list into an array
        //String[] answersToArray = new String[question.getAnswers().size()];
        //question.getAnswers().toArray(answersToArray);

        // Create a bundle to hold arguments
        Bundle args = new Bundle();
        args.putString(QUESTION_TEXT, question.getQuestion());
        //args.putStringArray(QUESTION_ANSWERS, answersToArray);
        args.putInt(QUESTION_ID, question.getId());

        // create a fragment and set arguements to it
        SelectionFragment fragment = new SelectionFragment();
        fragment.setArguments(args);
        return fragment;

    }

    @Override
    public void onCreate( Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // if fragment was created with arguements, assignment to respective variables
        if (getArguments() != null) {
            qID = getArguments().getInt(QUESTION_ID);
            questionText = getArguments().getString(QUESTION_TEXT);
            //answers = getArguments().getStringArray(QUESTION_ANSWERS);
            Log.i("Question ID",String.valueOf(qID));
        }
    }

    public static int getResId(String resName, Class<?> c) {

        try {
            Field idField = c.getDeclaredField(resName);
            return idField.getInt(idField);
        } catch (Exception e) {
            Log.e("SELECTION FRAGMENT", "Error getting image resource " + e.toString());
            return -1;
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.selection_question, container, false);

        final TextView questionTV = (TextView) view.findViewById(R.id.title_selection_question);
        questionTV.setText(questionText);

        // the image view that changes with the value of the seek bar
        indicator = (ImageView) view.findViewById(R.id.emotionIndicator);

        // find the seek bar and set a change listener to tack the value
        seekBar = (SeekBar) view.findViewById(R.id.seekBar);
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {

            // get the value of the seekbar
            // use that value to get the image from the satisfaction array
            // set image resource
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                indicator.setImageResource(getResources().getIdentifier(satisfaction[seekBar.getProgress()], "drawable", getActivity().getPackageName()));
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        return view;
    }
}