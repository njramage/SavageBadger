package com.savage_badger.survey_badger;

import android.os.AsyncTask;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.ListIterator;

import HTTPCom.httpCom;

public class MainActivity extends AppCompatActivity {

    private JSONObject jsonObject;
    private List<Question> questionsList;
    private List<Answer> answersList;
    private int currentQuestion;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        currentQuestion = 1;// Start at first question
    }

    // gets survey questions as a JSON object
    public void getSurvey() {
        // reset questions and answers
        questionsList = new ArrayList<Question>();

        answersList = new ArrayList<Answer>();

        jsonObject = null;//TODO: fetch JSON object with questions
        createQuestions(jsonObject);
    }

    // Creates a list of question objects
    public void createQuestions(JSONObject jsonObject) {

        try {

            JSONArray questions = jsonObject.getJSONArray("questions");

            // fill questions list
            for (int i = 0; i < questions.length(); i++) {
                JSONObject q = questions.getJSONObject(i);

                JSONObject answersJSON = q.getJSONObject("answers");
                try {
                    JSONArray answers = answersJSON.getJSONArray("answers");

                    List<String> possibleAnswers = new List<String>() {
                        @Override
                        public int size() {
                            return 0;
                        }

                        @Override
                        public boolean isEmpty() {
                            return false;
                        }

                        @Override
                        public boolean contains(Object o) {
                            return false;
                        }

                        @NonNull
                        @Override
                        public Iterator<String> iterator() {
                            return null;
                        }

                        @NonNull
                        @Override
                        public Object[] toArray() {
                            return new Object[0];
                        }

                        @NonNull
                        @Override
                        public <T> T[] toArray(T[] a) {
                            return null;
                        }

                        @Override
                        public boolean add(String s) {
                            return false;
                        }

                        @Override
                        public boolean remove(Object o) {
                            return false;
                        }

                        @Override
                        public boolean containsAll(Collection<?> c) {
                            return false;
                        }

                        @Override
                        public boolean addAll(Collection<? extends String> c) {
                            return false;
                        }

                        @Override
                        public boolean addAll(int index, Collection<? extends String> c) {
                            return false;
                        }

                        @Override
                        public boolean removeAll(Collection<?> c) {
                            return false;
                        }

                        @Override
                        public boolean retainAll(Collection<?> c) {
                            return false;
                        }

                        @Override
                        public void clear() {

                        }

                        @Override
                        public String get(int index) {
                            return null;
                        }

                        @Override
                        public String set(int index, String element) {
                            return null;
                        }

                        @Override
                        public void add(int index, String element) {

                        }

                        @Override
                        public String remove(int index) {
                            return null;
                        }

                        @Override
                        public int indexOf(Object o) {
                            return 0;
                        }

                        @Override
                        public int lastIndexOf(Object o) {
                            return 0;
                        }

                        @Override
                        public ListIterator<String> listIterator() {
                            return null;
                        }

                        @NonNull
                        @Override
                        public ListIterator<String> listIterator(int index) {
                            return null;
                        }

                        @NonNull
                        @Override
                        public List<String> subList(int fromIndex, int toIndex) {
                            return null;
                        }
                    };

                    // fill answers list
                    for (int j = 0; j < answers.length(); j++) {
                        String possibleAnswer = answers.getString(j);
                        possibleAnswers.add(possibleAnswer);
                    }

                    Question question = new Question(q.getInt("id"), q.getString("question"), q.getString("type"), possibleAnswers);

                    questionsList.add(question);

                } catch (JSONException e) {
                    //TODO: Exception message
                }
            }
        } catch (JSONException e) {
            //TODO: Exception message
        }
    }

    //Server connection tasks
    private class fetchTask extends AsyncTask<Integer, JSONObject, JSONObject> {

        @Override
        protected void onPreExecute() {
            //Update GUI before execute
        }

        @Override
        protected JSONObject doInBackground(Integer... params) {
            JSONObject res = null;
            res = httpCom.getSurvey(params[0]);
            return res;
        }

        @Override
        protected void onPostExecute(JSONObject s) { createQuestions(s); }
    }

}
