package com.blank_canvas.nathan_pc.location_alarm;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

/**
 * Created by Nathan on 30/03/2016.
 */
public class AlarmActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_alarm);
    }

    @Override
    protected void onStart() {
        super.onStart();
        TextView tv = (TextView) findViewById(R.id.done_text);
        tv.setText(CheckLocation.getSuburb());
    }
}
