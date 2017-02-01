package com.savage_badger.survey_badger;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentManager;
import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.widget.TextView;

import android.util.Log;

/**
 * Created by nathan on 27/01/17.
 */

public class SelectionFragment extends Fragment {

    // Tags to help find the arguements the fragment was initialised with
    private static final String QUESTION_TEXT = "QUESTION_TEXT";
    private static final String QUESTION_ANSWERS = "QUESTION_ANSWERS";

    private String[] answers;
    private String questionText;

    private int test = 1;
    private int person_id = 1;// defualt player id for testing
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

        final TextView questionTV = (TextView) view.findViewById(R.id.title_selection_question);
        questionTV.setText(questionText);



       int numRows = (int) answers.length;
        if (answers.length % 3 != 0)
        {
            numRows++;
        }
        RelativeLayout mRelativeLayout = (RelativeLayout) view.findViewById(R.id.button_container);
        for (int i = 0; i < answers.length; i++) ///  THE ISSUE IS THAT ITS CREATING THE BUTTON ONCE AND JUST OVER LAPING IT
        {


          //  for (int j = 0; j<answers.length;j++)
            //{
                int layoutMarginLeft = 180;
                int layoutMarginTop = 180;
                int layoutMaringRight = 180;
                int layoutMaringBottom = 0;
                if (test == 2)
                {


                    layoutMarginLeft = 580;

                }
                else if (test == 3)
                {
                    layoutMarginLeft = 980;
                    //ayoutMaringRight = 580;

                }
                else if (test == 4)
                {
                    layoutMarginTop = 380;

                }
                else if (test == 5)
                {
                    layoutMarginTop = 380;
                    layoutMarginLeft = 580;
                }
                else if (test == 6)
                {
                    layoutMarginTop = 380;
                    layoutMarginLeft = 980;
                }
                else if (test == 7)
                {
                    layoutMarginTop = 580;
                }



                Context mContext = getContext();
             //   Button button = new Button(mContext);
               // Button btn = new Button(mContext);
               // Button btn = new Button (mContext);
                int paddingTopPixels = 90;
                int paddingLeftPixels = 60;

                float density = getContext().getResources().getDisplayMetrics().density;
                int paddingTopDp=(int) (paddingTopPixels * density);
                int paddingLeftDp =(int) (paddingLeftPixels * density);

               // button.setPadding(paddingLeftDp, 0, paddingLeftDp, 0);//LEFT, TOP, RIGHT, BOTTOM
               // btn.setPaddingRelative(0, paddingLeftDp, 0, paddingTopDp);
               // btn.setLayoutParams();
              //  mRelativeLayout.addView(button);
                //mRelativeLayout.addView(btn);
              //  button.setText("hi");
               // btn.setText("bye");

                //SET DIFFERENT VARRIABLES, WHEN IT INCREMENTS THROUGH THE FOR LOOP CHANGE THE VARIABLES.


                Button btn = new Button(mContext);

                RelativeLayout.LayoutParams layoutParams = new RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.WRAP_CONTENT, RelativeLayout.LayoutParams.WRAP_CONTENT);
                layoutParams.addRule(RelativeLayout.ALIGN_PARENT_TOP);
                layoutParams.setMargins(layoutMarginLeft, layoutMarginTop, layoutMaringRight, layoutMaringBottom);

                  btn.setLayoutParams(layoutParams);
                Log.i("test",  answers.clone().toString());
               // Log.i ("testing", questionText.toString());
                mRelativeLayout.addView(btn);
               // btn.setText(  answers.toString());
                btn.setText("test");
                //answers.toString().indexOf(1);


                test++;
               // String hello = toString().test;
               // Log.i ("test", test );
            //((MainActivity)getActivity()).pickNumber(view);


            btn.setOnClickListener(new View.OnClickListener() {
                public void onClick(View view) {
                    // Perform action on click
                    Log.i ("testing", "will this work");
                    //((MainActivity)getActivity()).saveAnswer(questionTV, person_id, answers.toString());
                    ((MainActivity)getActivity()).selectionQuestion(view)  ;
                }
            });


           // }
        }
      /*  RelativeLayout mRelativeLayout = (RelativeLayout) view.findViewById(R.id.button_container);

       for (int i = 0; i < answers.length; i++) {
            Context mContext = getContext();
            Button btn = new Button(mContext);



            RelativeLayout.LayoutParams layoutParams = new RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.WRAP_CONTENT, RelativeLayout.LayoutParams.WRAP_CONTENT);
            layoutParams.addRule(RelativeLayout.ALIGN_TOP);

            btn.setLayoutParams(layoutParams);

            mRelativeLayout.addView(btn);
            btn.setText(answers.toString());

        }*/

        return view;
    }
}
