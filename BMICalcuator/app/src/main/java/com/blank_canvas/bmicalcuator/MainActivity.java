package com.blank_canvas.bmicalcuator;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.RadioButton;
import android.widget.RadioGroup;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void submit(View view) {
        double bmi = calculateBMI(0,0,"Male");
        Intent intent = new Intent(this, DisplayBMI.class);

    }

    private double calculateBMI(int height, int weight, String gender) {
        return 0;
    }
}
