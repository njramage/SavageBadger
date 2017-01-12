package HTTPCom;

import android.util.Base64;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

public class httpCom {
	//Connection BASEURL
	final static String BASEURL = "";

    final static int CONNECTTIMEOUT = 8000;
    final static int SOCKETTIMEOUT = 7000;

    public static JSONObject sendAnswers(JSONArray data) {

        BufferedReader reader = null;
        HttpURLConnection con = null;

        JSONArray postData = data;

        Log.i("JSON", postData.toString());
        //int postDataLength = postData.length;
        try {
            URL url = new URL(BASEURL + "submitsurvey/");
            Log.i("httpCOM", "Connecting to: " + url);
            HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
            httpURLConnection.setDoOutput(true);
            httpURLConnection.setDoInput(true);
            httpURLConnection.setInstanceFollowRedirects(false);
            httpURLConnection.setRequestMethod("POST");
            httpURLConnection.setRequestProperty("Content-Type",
                    "application/json");
            //httpURLConnection.setRequestProperty("charset", "utf-8");
            //httpURLConnection.setRequestProperty("Content-Length",
            //       Integer.toString(postDataLength));
            httpURLConnection.setConnectTimeout(10000);
            DataOutputStream dataOutputStream = new DataOutputStream(
                    httpURLConnection.getOutputStream());
            dataOutputStream.write(postData.toString().getBytes("UTF-8"));
            dataOutputStream.flush();
            dataOutputStream.close();
            int status = httpURLConnection.getResponseCode();
            Log.i("HTTP", "Response " + String.valueOf(status));
            if (status == HttpURLConnection.HTTP_OK) {
                InputStream responseStream = new BufferedInputStream(
                        httpURLConnection.getInputStream());
                BufferedReader responseStreamReader = new BufferedReader(
                        new InputStreamReader(responseStream));
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = responseStreamReader.readLine()) != null) {
                    sb.append(line);
                }

                JSONObject obj = new JSONObject(sb.toString());

                Log.i("JSON", obj.toString());
                if (obj.has("result")) {
                    return obj;
                } else {
                    Log.e("httpCOM", "No status tag in response");
                    JSONObject res = new JSONObject();
                    res.put("result", false);
                    return res;
                }
            }
            Log.e("httpCOM", "Response: " + String.valueOf(httpURLConnection.getResponseCode()));
            JSONObject res = new JSONObject();
            res.put("result", false);
            return res;

        } catch (Exception e) {
            e.printStackTrace();
            JSONObject res = new JSONObject();
            try {
                res.put("result", false);
                return res;
            } catch (JSONException e1) {
                e1.printStackTrace();
            }
            return null;
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                    return null;
                }
            }
        }
    }

    public static JSONObject getSurvey(int id) {

        BufferedReader reader = null;
        HttpURLConnection con = null;

        try {
            URL url = new URL(BASEURL + "/getsurvey/" + String.valueOf(id));
            con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("GET");

            //Set timeout
            con.setConnectTimeout(CONNECTTIMEOUT);
            con.setReadTimeout(SOCKETTIMEOUT);

            StringBuilder sb = new StringBuilder();
            reader = new BufferedReader((new InputStreamReader(con.getInputStream())));

            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line);
            }
            JSONObject obj = new JSONObject(sb.toString());

            if (obj.has("questions")) {
                return obj;
            } else {
                Log.e("httpCon", "Retrieving Questions failed");
                JSONObject handle = new JSONObject().put("result", false);
                return handle;
            }
        } catch (Exception e) {
            e.printStackTrace();
            try {
                int status = con.getResponseCode();
            } catch (IOException e1) {
                e1.printStackTrace();
            }
            return null;
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                    return null;
                }
            }
        }
    }

}


