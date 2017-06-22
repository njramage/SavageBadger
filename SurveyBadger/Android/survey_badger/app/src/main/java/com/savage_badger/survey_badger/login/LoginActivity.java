package com.savage_badger.survey_badger.login;

import android.content.Intent;
import android.os.Bundle;
import android.os.PersistableBundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.savage_badger.survey_badger.MainActivity;
import com.savage_badger.survey_badger.R;

import java.util.zip.Inflater;

/**
 * Created by nrama on 22/06/2017.
 */

public class LoginActivity extends AppCompatActivity {

    private View login_view;
    private Button login_btn;
    private EditText username, password;
    private int counter = 10;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        login_view = getLayoutInflater().inflate(R.layout.login, null);
        setContentView(login_view);
        login_btn = (Button)findViewById(R.id.login_btn);

        username = (EditText)findViewById(R.id.username);
        password = (EditText)findViewById(R.id.password);
    }

    /*
     * Description: Login checks the enterd credentials against the user credentials in a database.
     *              If there are correct then the user can login, else the attempts counter is
     *              decremented.  If the coutner reeaches zero then the login button is disabled and
     *              the application exits.
     * Input: The the layout layout as a view
     * Output: None
     */
    public void login(View view) {
        //TODO: add proper login authentication
        if (username.getText().toString().equals("admin") && password.getText().toString().equals("admin")) {
            //correcct password

            int userid = 1;

            Intent intent = new Intent(getBaseContext(), MainActivity.class);
            intent.putExtra("userid", userid);
            startActivity(intent);

        } else {
            //wrong password
            counter--;// Decremment login attempt counter

            if(counter==0)// No more login attempts allowed
                login_btn.setEnabled(false);// Desable login button
                finish();// Call onDestroy lifecycle activity
        }
    }

    /*
     * Description: Cleans up activity and closes the app
     * Input: Input: The the login layout as a view
     * Output: None
     */
    public void cancel(View view) {
        finish();// Call onDestroy
    }
}
