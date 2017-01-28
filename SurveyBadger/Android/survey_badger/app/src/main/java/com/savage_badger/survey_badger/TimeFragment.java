package com.savage_badger.survey_badger;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

/**
 * Created by nathan on 28/01/17.
 */

public class TimeFragment extends Fragment {

    private static final String QUESTION_TEXT = "QUESTION_TEXT";

    private String question_text;

    public TimeFragment() {

    }

    public static TimeFragment newInstance(Question question) {

        Bundle args = new Bundle();
        args.putString(QUESTION_TEXT, question.getQuestion());

        TimeFragment fragment = new TimeFragment();
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (getArguments() != null) {
            question_text = getArguments().getString(QUESTION_TEXT);
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.time_set_question, container, false);
        TextView questionTV = (TextView) view.findViewById(R.id.title_time_set_question);
        questionTV.setText(question_text);

        return view;
    }
}
