package com.savage_badger.survey_badger;

import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.widget.TextView;

/**
 * Created by nathan on 27/01/17.
 */

public class SelectionFragment extends Fragment {

    // Tags to help find the arguements the fragment was initialised with
    private static final String QUESTION_TEXT = "QUESTION_TEXT";
    private static final String QUESTION_ANSWERS = "QUESTION_ANSWERS";

    private String[] answers;
    private String questionText;

    public SelectionFragment () {

    }

    public static SelectionFragment newInstance(Question question) {

        // Translate answers list into an array
        String[] answersToArray = new String[question.getAnswers().size()];
        question.getAnswers().toArray(answersToArray);

        // Create a bundle to hold arguments
        Bundle args = new Bundle();
        args.putString(QUESTION_TEXT, question.getQuestion());
        args.putStringArray(QUESTION_ANSWERS, answersToArray);

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
            questionText = getArguments().getString(QUESTION_TEXT);
            answers = getArguments().getStringArray(QUESTION_ANSWERS);
        }
    }

    //TODO: finish button set up
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.selection_question, container, false);

        TextView questionTV = (TextView) view.findViewById(R.id.title_selection_question);
        questionTV.setText(questionText);


        RelativeLayout mRelativeLayout = (RelativeLayout) view.findViewById(R.id.button_container);

       for (int i = 0; i < answers.length; i++) {
            Context mContext = getContext();
            Button btn = new Button(mContext);



            RelativeLayout.LayoutParams layoutParams = new RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.WRAP_CONTENT, RelativeLayout.LayoutParams.WRAP_CONTENT);
            layoutParams.addRule(RelativeLayout.ALIGN_TOP);

            btn.setLayoutParams(layoutParams);

            mRelativeLayout.addView(btn);
            btn.setText(answers.toString());

        }


        return view;
    }
}
