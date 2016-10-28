package com.blank_canvas.location_alarm;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void searchForLocation(View view) {
        TextView suburbText = (TextView)findViewById(R.id.suburb);
        Button searchButton = (Button)findViewById(R.id.suburb_button);

        if (suburbText.getText() != null) {
            searchButton.setEnabled(false);
        }
        else {
        }
    }
}
