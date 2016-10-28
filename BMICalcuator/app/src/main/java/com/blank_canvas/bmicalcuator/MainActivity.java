package com.blank_canvas.bmicalcuator;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;

public class MainActivity extends AppCompatActivity {

    public final static String EXTRA_GENDER = "Gender";
    public final static String EXTRA_BMI = "BMI";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void submit(View view) {

        /* Get selected gender */
        RadioGroup genderGroup = (RadioGroup) findViewById(R.id.gender_radiogroup);
        int genderId = genderGroup.getCheckedRadioButtonId();
        RadioButton genderRadio = (RadioButton) findViewById(genderId);
        String gender = genderRadio.getText().toString();

        /* Get entered height */
        EditText heightText = (EditText) findViewById(R.id.height_textfield);
        double height = Double.parseDouble(heightText.getText().toString());

        /* Get entered weight */
        EditText weightText = (EditText) findViewById(R.id.weight_textfield);
        double weight = Double.parseDouble(heightText.getText().toString());

        double bmi = calculateBMI(height, weight, gender); // calulate BMI

        /* Start Display BMI activity and send the BMI and gender to it */
        Intent intent = new Intent(this, DisplayBMI.class);
        intent.putExtra("Gender", gender);
        intent.putExtra("BMI", bmi);
        startActivity(intent);
    }

    private double calculateBMI(double height, double weight, String gender) {
        return 0;
    }
}
