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
import android.widget.ImageButton;
import android.widget.RelativeLayout;
import android.widget.TextView;

import android.util.Log;

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
            answers = getArguments().getStringArray(QUESTION_ANSWERS);
            Log.i("Question ID",String.valueOf(qID));
        }
    }

    //TODO: finish button set up
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.selection_question, container, false);

        final TextView questionTV = (TextView) view.findViewById(R.id.title_selection_question);
        questionTV.setText(questionText);



        int numRows = (int) answers.length / 3;// number of rows needed
        int numCols = answers.length / 3;// used to track number of 3 button rows
        Log.i ("answer Length", Integer.toString(answers.length));
        Log.i ("answer Length", Integer.toString(answers.length / 3));
        if (answers.length % 3 != 0)
        {
            numRows++;
        }
        int current_answer = 0;// current index for the possible answers
        RelativeLayout mRelativeLayout = (RelativeLayout) view.findViewById(R.id.button_container);
        for (int i = 0; i < numRows; i++)
        {
            int numBtns;
            if (numCols > 0)// the row needs 3 buttons
            {
                numBtns = 3;
            }
            else// calcualte how many buttons the row should have
            {
                numBtns = numRows % 3;

            }
            for (int j = 0; j < numBtns; j++) {
                int layoutMarginLeft = 30 + (100 * (j));
                int layoutMarginTop = 30 + (80 * (i));
                int layoutMaringRight = 0;
                int layoutMaringBottom = 0;


                Context mContext = getContext();

                float density = getContext().getResources().getDisplayMetrics().density;
                layoutMarginLeft = (int) (layoutMarginLeft * density);
                layoutMarginTop = (int) (layoutMarginTop * density);


              //  Button btn = new Button(mContext);
                ImageButton btn = new ImageButton(mContext);

                RelativeLayout.LayoutParams layoutParams = new RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.WRAP_CONTENT, RelativeLayout.LayoutParams.WRAP_CONTENT);
                layoutParams.addRule(RelativeLayout.ALIGN_PARENT_TOP);
                layoutParams.addRule(RelativeLayout.ALIGN_PARENT_LEFT);
                layoutParams.setMargins(layoutMarginLeft, layoutMarginTop, layoutMaringRight, layoutMaringBottom);

                btn.setLayoutParams(layoutParams);
                Log.i("test", answers.toString());
                mRelativeLayout.addView(btn);

               // btn.setText(answers[current_answer]);

                ///ISSUES LEFT
                ///HAVING IT DYNAMICALLY SET BUTTON IMAGES
                ///IMAGE PLACING ON SCREENS.


                final String btnAnswer = answers[current_answer];
                Log.i ("testing string output", btnAnswer);
                Log.i ("testing string output", "Bus");

                int buttonImage = 0; // R.drawable.bus;
              //  Log.i("what is the int", Integer.toString(H));
              //   H = R.drawable.car;

              //  Log.i("what is the int", Integer.toString(H));
             //   int J =  2130837587;

               // btn.setImageResource(H);

               //if (answers[current_answer].equals(current_answer+".jpg"))
                if (answers[current_answer].equals("Bus"))
                {
                    buttonImage = R.drawable.bus;
                    //  btn.setImageResource(buttonImage);
                    btn.setImageBitmap(    ((MainActivity)getActivity()).BitmapImages().get(0));
                }

                else if (answers[current_answer].equals("Car"))
                {
                    buttonImage = R.drawable.car;
                    btn.setImageBitmap(    ((MainActivity)getActivity()).BitmapImages().get(1));
                }
                else if(answers[current_answer].equals("Ferry"))
                {
                    buttonImage = R.drawable.ferry;
                      btn.setImageResource(buttonImage);
                }
                else if (answers[current_answer].equals("Train"))
                {
                    buttonImage = R.drawable.train;
                      btn.setImageResource(buttonImage);
                }
                else if (answers[current_answer].equals("Tram"))
                {
                    buttonImage = R.drawable.tram;
                      btn.setImageResource(buttonImage);
                }






              /*  if (answers[current_answer].equals("Bus") )
                {
                    Log.i ("does it get in", "yes");
                    btn.setImageResource(R.drawable.images1);
                }
                else
                {
                    btn.setImageResource(R.drawable.download);
                }*/
                //having buttons as they own unquie image
                // having the pressed button be saved and sent back.






                btn.setOnClickListener(new View.OnClickListener() {
                    public void onClick(View view) {
                        // Perform action on click
                        Log.i("testing", "will this work");
                       // Button b = (Button) view;
                       // ((MainActivity) getActivity()).saveAnswer(qID, person_id, b.getText().toString());
                        ((MainActivity) getActivity()).saveAnswer(qID, person_id, btnAnswer);
                        ((MainActivity) getActivity()).selectionQuestion(view);
                        Log.i ("did they get the answer", btnAnswer);
                    }
                });

                current_answer++;
            }
           
            numCols--;
        }

        return view;
    }
}
/*
    ImageButton btn = new ImageButton(mContext);
    Button btnTest = new Button (mContext);

    RelativeLayout.LayoutParams layoutParams = new RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.WRAP_CONTENT, RelativeLayout.LayoutParams.WRAP_CONTENT);
layoutParams.addRule(RelativeLayout.ALIGN_PARENT_TOP);
        layoutParams.addRule(RelativeLayout.ALIGN_PARENT_LEFT);
        layoutParams.setMargins(layoutMarginLeft, layoutMarginTop, layoutMaringRight, layoutMaringBottom);

        btn.setLayoutParams(layoutParams);
        Log.i("test", answers.toString());
        mRelativeLayout.addView(btn);
        // Drawable myDrawable = getResources().getDrawable(R.drawable.download);

        // Drawable myDrawable = getResources().getDrawable(<insert your id here>);e =
        // btn.setImageDrawable(@drawable/download.png);
        //   btn.setImageDrawable(android.graphics.drawable.Drawable.createFromPath("@drawablhjkhkjhkhhkjhkhje/download"));
        btnTest.setText(answers[current_answer]);
        String testString = answers[current_answer];
        Log.i ("testing string output", testString);
        Log.i ("testing string output", "Bus");

        if (answers[current_answer].equals("Bus") )
        {
        Log.i ("does it get in", "yes");
        btn.setImageResource(R.drawable.apple);
        }
        //having buttons as they own unquie image
        // having the pressed button be saved and sent back.



                */
/*else if (testString == "Bus" || testString == "Car"|| testString == "Tram")
                {
                    btn.setImageResource(R.drawable.apple);
                }*//*



        // btn.setImageResource(R.drawable.download);
        Log.i ("set the image", "yes");

        // btn.setText(answers[current_answer]);




        btn.setOnClickListener(new View.OnClickListener() {
public void onClick(View view) {
        // Perform action on click
        Log.i("testing", "will this work");
        //  ImageButton b = (ImageButton) view;
        // ((MainActivity) getActivity()).saveAnswer(qID, person_id, b.getText().toString());
        ((MainActivity) getActivity()).selectionQuestion(view);
        }
        });
*/