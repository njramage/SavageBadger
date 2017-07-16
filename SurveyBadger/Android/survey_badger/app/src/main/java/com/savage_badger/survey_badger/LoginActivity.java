package com.savage_badger.survey_badger;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Parcel;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;

/**
 * Created by nathan on 15/07/17.
 */

public class LoginActivity extends AppCompatActivity {

    private static final String TAG = "Login Activity";
    private static final String LOGIN_FRAGMENT = "login framgent";

    private View login_view, code_check, login_act_view;
    private ArrayList<Question> questionsList;
    private String survey;

    /*
   * Login varibles
   */
    private Button login_btn;
    private EditText username, password;
    private int counter = 10;

    /*
     * Code Check variables
     */
    private EditText entered_code;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        login_act_view = getLayoutInflater().inflate(R.layout.activity_login, null);
        login_view = getLayoutInflater().inflate(R.layout.fragment_login, null);
        code_check = getLayoutInflater().inflate(R.layout.code_check, null);

        setContentView(login_act_view);

        displayLogin();
    }

    /*
     * Name: displayLogin
     * Description: Displays the login fragment
     * Input: None
     * Output: None
     */
    public void displayLogin() {
        FragmentManager fm = getSupportFragmentManager();
        FragmentTransaction ft = fm.beginTransaction();

        // Create a new instance of a login fragment
        LoginFragment loginFrag = new LoginFragment();
        ft.add(R.id.login_container, loginFrag, LOGIN_FRAGMENT);
        ft.commit();
    }// End displayLogin()

    /*
     * Name: Login
     * Description: Login checks the enterd credentials against the user credentials in a database.
     *              If there are correct then the user can login, else the attempts counter is
     *              decremented.  If the coutner reeaches zero then the login button is disabled and
     *              the application exits.
     * Input: The the layout layout as a view
     * Output: None
     */
    public void login(View view) {
        // TODO: 22/06/2017 Add proper login authentication
        username = (EditText) findViewById(R.id.username);
        password = (EditText) findViewById(R.id.password);

        LoginActivity.loginTask loginTask = new LoginActivity.loginTask();

        try {
            Boolean result = loginTask.execute(username.getText().toString(), password.getText().toString()).get();
            Log.i(TAG, "Usersname: " + username.getText().toString() + "/");
            Log.i(TAG, "password: " + password.getText().toString() + "/");
            if (result) {
                //correcct password
                Log.i(TAG, "Login correct!");

                login_btn = (Button) findViewById(R.id.login_btn);
                login_btn.setEnabled(false);
                displayCodeCheck();
            } else {
                //wrong password
                counter--;// Decremment login attempt counter

                Log.d(TAG, "Wrong password or usename");

                if (counter == 0) {// No more login attempts allowed
                    login_btn.setEnabled(false);// Desable login button
                    finish();// Call onDestroy()
                }
            }
        } catch (InterruptedException e) {
            Log.e(TAG, "Interrupted: " + e);
        } catch (ExecutionException e) {
            Log.e(TAG, "Execution Expection: " + e);
        }

    }// End login()

    /*
     * Name: displayCodeCheck
     * Description: Displays the code check fragment
     * Input: None
     * Output: None
     */
    public void displayCodeCheck() {
        FragmentManager fm = getSupportFragmentManager();
        Fragment fragment = fm.findFragmentByTag(LOGIN_FRAGMENT);// find any active fragments with the QUESTION_FRAGMENT tag
        FragmentTransaction ft = fm.beginTransaction().setTransition(FragmentTransaction.TRANSIT_FRAGMENT_FADE);

        // Create a new instance of a login fragment
        CodeFragment codefrag = new CodeFragment();

        // if there are is an active fragment, replace the old fragment with the new one and commit
        if (fragment != null) {
            ft.replace(R.id.login_container, codefrag, LOGIN_FRAGMENT);
            ft.commit();
        } else {// add the new framgent and commit
            ft.add(R.id.login_container, codefrag, LOGIN_FRAGMENT);
            ft.commit();
        }

    }// End displayCodeCheck()

    /*
     * Description: Checks the code entered by the user is a vaild survey code
     * Input: The layout layout as a view
     * Output: None
     */
    public void code_continue(View view) {
        LoginActivity.fetchTask getQuestions = new LoginActivity.fetchTask();

        entered_code = (EditText) findViewById(R.id.code_check);

        this.survey = entered_code.getText().toString();
        getQuestions.execute(this.survey);
    }// End code_continue()

    /*
     * Name: show_signup
     * Description: Displays the signup fragment
     * Input: None
     * Output: None
     */
    public void show_signup(View view) {
        FragmentManager fm = getSupportFragmentManager();
        Fragment fragment = fm.findFragmentByTag(LOGIN_FRAGMENT);// find any active fragments with the QUESTION_FRAGMENT tag
        FragmentTransaction ft = fm.beginTransaction().setTransition(FragmentTransaction.TRANSIT_FRAGMENT_FADE).addToBackStack(null);

        // Create a new instance of a login fragment
        SignUpFragment signUpFragment = new SignUpFragment();

        // if there are is an active fragment, replace the old fragment with the new one and commit
        if (fragment != null) {
            ft.replace(R.id.login_container, signUpFragment, LOGIN_FRAGMENT);
            ft.commit();
        } else {// add the new framgent and commit
            ft.add(R.id.login_container, signUpFragment, LOGIN_FRAGMENT);
            ft.commit();
        }

    }// End show_sinup()

    /*
     * Name: signup
     * Description: Checks user input and signs the user up
     * Input: The layout layout as a view
     * Output: None
     */
    public void signup(View view) {
        EditText signupUser = (EditText) findViewById(R.id.new_username);
        EditText signupPass = (EditText) findViewById(R.id.new_password);
        EditText confirmPass = (EditText) findViewById(R.id.confirm_password);
        EditText email = (EditText) findViewById(R.id.email);
        TextView errortext = (TextView) findViewById(R.id.textView);
        String errors = "";

        if (signupUser.getText().length() <= 0) {
            signupUser.setBackground(ContextCompat.getDrawable(this.getApplicationContext(), R.drawable.textbox_background_error));
            errors += "- Enter a Username\n";
        }

        if (signupPass.getText().length() <= 0) {
            signupPass.setBackground(ContextCompat.getDrawable(this.getApplicationContext(), R.drawable.textbox_background_error));
            errors += "- Enter a Password\n";
        } else if (!confirmPass.getText().toString().equals(signupPass.getText().toString())) {
            signupPass.setBackground(ContextCompat.getDrawable(this.getApplicationContext(), R.drawable.textbox_background_error));
            confirmPass.setBackground(ContextCompat.getDrawable(this.getApplicationContext(), R.drawable.textbox_background_error));
            errors += "- Passwords to not match\n";
        }

        if (email.getText().length() <= 0) {
            email.setBackground(ContextCompat.getDrawable(this.getApplicationContext(), R.drawable.textbox_background_error));
            errors += "- Enter an Email\n";
        }

        if (errors.length() > 0) {
            errortext.setText(errors);
        } else {
            LoginActivity.signupTask signup = new LoginActivity.signupTask();
            signup.execute(signupUser.getText().toString(), signupPass.getText().toString(), confirmPass.getText().toString(), email.getText().toString());
            Button signupbtn = (Button) findViewById(R.id.signupnow_btn);
            signupbtn.setText("Signing up...");
            signupbtn.setEnabled(false);
        }
    }// End signup()

    /*
     * Name: clearTextFields
     * Description: Clears the password fields if the user already exists and enables signup button
     *              again
     * Input: None
     * Output: None
     */
    private void clearTextFields() {
        EditText clearPass = (EditText) findViewById(R.id.new_password);
        EditText clearConfirmPass = (EditText) findViewById(R.id.confirm_password);
        Button signupbtn = (Button) findViewById(R.id.signupnow_btn);

        clearPass.setText("");
        clearConfirmPass.setText("");
        signupbtn.setText(R.string.signup);
        signupbtn.setEnabled(true);
    }

    //Server connection tasks
    private class fetchTask extends AsyncTask<String, ArrayList<Question>, ArrayList<Question>> {

        @Override
        protected void onPreExecute() {
            //Update GUI before execute
        }

        @Override
        protected ArrayList<Question> doInBackground(String... params) {
            QuestionList questionListCreator = new QuestionList();
            ArrayList<Question> questions = new ArrayList<Question>();
            JSONObject s = httpCom.getSurvey(params[0]);
            Log.i(TAG, "getting survey with code");
            try {
                Log.i(TAG, "code: " + params[0]);
                if (s.has("questions")) {

                    survey = String.valueOf(s.getInt("survey"));
                    Log.i(TAG, "Survey id is: " + survey);

                    //Create question list
                    questionListCreator.createQuestions(s);
                    Log.i("Polavo", "first question: " + questionListCreator.getQustionList().get(0));
                } else {
                    Log.e("Polavo", "Error occured getting the survey from the server");
                }
            } catch (Exception e) {
                Log.e("Polavo", "Error occured getting the survey from the server: " + e.toString());
            }
            Log.i(TAG, "return statement");
            return questionListCreator.getQustionList();
        }

        @Override
        protected void onPostExecute(ArrayList<Question> questions) {
            questionsList = questions;
            if (questionsList != null) {
                Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                Bundle bundle = new Bundle();
                bundle.putParcelableArrayList("questions", questionsList);
                bundle.putString("survey", survey);
                intent.putExtras(bundle);
                startActivity(intent);
            } else {
                Toast.makeText(LoginActivity.this, "Wrong code, try again", Toast.LENGTH_SHORT).show();
            }
        }
    }// End fetchTask()

    private class loginTask extends AsyncTask<String, Boolean, Boolean> {

        @Override
        protected Boolean doInBackground(String... params) {

            Log.i(TAG, "Login");
            // Send user and pass to be checked by server
              /*
              * Create JSON object
              * Username : <Username entered by user>
              * Password : <Password entered by user>
              */

            try {
                JSONObject loginDetails = new JSONObject();
                loginDetails.put("username", params[0].toString());
                loginDetails.put("password", params[1].toString());

                JSONObject result = httpCom.login(loginDetails);

                //Check the result of the query
                if (result.has("status")) {
                    return result.getBoolean("status");
                } else {
                    return false;
                }
            } catch (JSONException e) {
                Log.e(TAG, "JSON Exception: ", e);
                return false;
            }
        }

        }// End loginTask()

    private class signupTask extends AsyncTask<String, Boolean, Boolean> {

        @Override
        protected Boolean doInBackground(String... params) {

            Log.i(TAG, "Signup");
            // Send user and pass to be checked by server
              /*
              * Create JSON object
              * Username : <Username entered by user>
              * Password : <Password entered by user>
              */

            try {
                JSONObject loginDetails = new JSONObject();
                loginDetails.put("username", params[0].toString());
                loginDetails.put("password", params[1].toString());
                loginDetails.put("confirmPass", params[2].toString());
                loginDetails.put("email", params[3].toString());

                JSONObject result = httpCom.signup(loginDetails);

                //Check the result of the query
                if (result.has("status")) {
                    return result.getBoolean("status");
                } else {
                    return false;
                }
            } catch (JSONException e) {
                Log.e(TAG, "JSON Exception: ", e);
                return false;
            }
        }

        @Override
        protected void onPostExecute(Boolean result) {
            if (!result) {
                Toast.makeText(LoginActivity.this, "Username or email already exists", Toast.LENGTH_SHORT).show();
                clearTextFields();// clears password fields and enables signup button again
            } else {
                Toast.makeText(LoginActivity.this, "User Created!", Toast.LENGTH_SHORT).show();
                FragmentManager fm = getSupportFragmentManager();
                fm.popBackStack();
            }
            Log.i("Polavo", "Login result: " + result.toString());
        }
    }// End signupTask()
}
