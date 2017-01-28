package com.savage_badger.survey_badger;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.NumberPicker;
import android.widget.TextView;

/**
 * Created by nathan on 27/01/17.
 */

public class NumberFragment extends Fragment {

    // Tags to help find the arguements the fragment was initialised with
    public static final String MAX_VALUE = "MAX_VALUE";
    public static final String QUESTION_TEXT = "QUESTION_TEXT";

    private String questionText;
    private int maxValue;// max value fot the numberpicker

    public NumberFragment() {

    }

    public static NumberFragment newInstance(Question question) {

        // Create a bundle to hold arguments
        Bundle args = new Bundle();
        args.putString(QUESTION_TEXT, question.getQuestion());
        args.putInt(MAX_VALUE, Integer.parseInt(question.getAnswers().get(0)));

        // create a fragment and set arguements to it
        NumberFragment fragment = new NumberFragment();
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceBundle) {
        super.onCreate(savedInstanceBundle);

        // if fragment was created with arguements, assignment to respective variables
        if (getArguments() != null) {
            questionText = getArguments().getString(QUESTION_TEXT);
            maxValue = getArguments().getInt(MAX_VALUE);
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

        // Inflate the frament's layout
        View view = inflater.inflate(R.layout.number_question, container, false);

        // Display the question text
        TextView questionTV = (TextView) view.findViewById(R.id.title_number_question);
        questionTV.setText(questionText);

        // Set up min and max values for the number picker
        NumberPicker numberPicker = (NumberPicker) view.findViewById(R.id.number_pick);
        numberPicker.setMinValue(0);
        numberPicker.setMaxValue(maxValue);

        return view;
    }
}
