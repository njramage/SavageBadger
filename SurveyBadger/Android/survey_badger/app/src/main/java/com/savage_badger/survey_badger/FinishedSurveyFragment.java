package com.savage_badger.survey_badger;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;

import java.util.ArrayList;

/**
 * Created by nathan on 28/01/17.
 */

public class FinishedSurveyFragment extends Fragment {

    private static final String QUESTION = "question";
    private static final String RATING = "rating";
    private String[] question, rating;

    public FinishedSurveyFragment () {

    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.finished_survey, container, false);
        return view;
    }
}
