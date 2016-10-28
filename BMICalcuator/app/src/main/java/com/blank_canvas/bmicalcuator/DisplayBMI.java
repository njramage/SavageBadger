package com.blank_canvas.bmicalcuator;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;

/**
 * Created by Nathan on 28/10/2016.
 */

public class DisplayBMI extends AppCompatActivity {

    private double bmi;
    private String gender;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.display_bmi);

        /* Get variables from intent */
        Intent intent = getIntent();
        gender = intent.getStringExtra(MainActivity.EXTRA_GENDER);
        bmi = intent.getDoubleExtra(MainActivity.EXTRA_BMI, 0);
    }
}
