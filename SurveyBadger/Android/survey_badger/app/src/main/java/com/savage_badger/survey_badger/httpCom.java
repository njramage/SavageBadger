package com.savage_badger.survey_badger;

import android.app.Activity;
import android.app.ActivityManager;
import android.content.ComponentName;
import android.content.Context;
import android.text.TextUtils;
import android.util.Base64;
import android.util.Log;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;

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
import java.net.CookieManager;
import java.net.HttpCookie;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class httpCom {
	//Connection BASEURL
	final static String BASEURL = "http://www.polavo.net/";

    final static int CONNECTTIMEOUT = 8000;
    final static int SOCKETTIMEOUT = 7000;


    static final String COOKIES_HEADER = "Set-Cookie";
    static final String COOKIE = "Cookie";

    static CookieManager msCookieManager = new CookieManager();

    public static JSONObject sendAnswers(JSONObject data) {


        BufferedReader reader = null;
        HttpURLConnection con = null;


        JSONObject postData = data;

        Log.i("JSON", postData.toString());
        //int postDataLength = postData.length;
        try {
            URL url = new URL(BASEURL + "submitsurvey/");
            Log.i("httpCOM", "Connecting to: " + url);
            con = (HttpURLConnection) url.openConnection();

            //Set timeout
            con.setConnectTimeout(CONNECTTIMEOUT);
            con.setReadTimeout(SOCKETTIMEOUT);

            con.setDoOutput(true);
            con.setDoInput(true);
            con.setInstanceFollowRedirects(false);
            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type",
                    "application/json");

            //set cookies
            if (msCookieManager.getCookieStore().getCookies().size() > 0) {
                //While joining the Cookies, use ',' or ';' as needed. Most of the server are using ';'
                con.setRequestProperty(COOKIE ,
                        TextUtils.join(";", msCookieManager.getCookieStore().getCookies()));
            }

            con.setConnectTimeout(10000);
            DataOutputStream dataOutputStream = new DataOutputStream(
                    con.getOutputStream());
            dataOutputStream.write(postData.toString().getBytes("UTF-8"));
            dataOutputStream.flush();
            dataOutputStream.close();

            //Get cookies from response
            Map<String, List<String>> headerFields = con.getHeaderFields();
            List<String> cookiesHeader = headerFields.get(COOKIES_HEADER);

            if (cookiesHeader != null) {
                for (String cookie : cookiesHeader) {
                    msCookieManager.getCookieStore().add(null, HttpCookie.parse(cookie).get(0));
                }
            }

            //Get and handle response code
            int status = con.getResponseCode();
            Log.i("HTTP", "Response " + String.valueOf(status));
            if (status == HttpURLConnection.HTTP_OK) {
                InputStream responseStream = new BufferedInputStream(
                        con.getInputStream());
                BufferedReader responseStreamReader = new BufferedReader(
                        new InputStreamReader(responseStream));
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = responseStreamReader.readLine()) != null) {
                    sb.append(line);
                }

                JSONObject obj = new JSONObject(sb.toString());

                Log.i("JSON", obj.toString());
                if (obj.has("status")) {
                    return obj;
                } else {
                    Log.e("httpCOM", "No status tag in response");
                    JSONObject res = new JSONObject();
                    res.put("status", false);
                    return res;
                }
            }
            Log.e("httpCOM", "Response: " + String.valueOf(con.getResponseCode()));
            JSONObject res = new JSONObject();
            res.put("status", false);
            return res;

        } catch (Exception e) {
            e.printStackTrace();
            JSONObject res = new JSONObject();
            try {
                res.put("status", false);
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

    public static JSONObject login(JSONObject data) {

        BufferedReader reader = null;
        HttpURLConnection con = null;

        JSONObject postData = data;

        Log.i("JSON", postData.toString());
        //int postDataLength = postData.length;
        try {
            URL url = new URL(BASEURL + "login");
            Log.i("httpCOM", "Connecting to: " + url);
            con = (HttpURLConnection) url.openConnection();

            //Set timeout
            con.setConnectTimeout(CONNECTTIMEOUT);
            con.setReadTimeout(SOCKETTIMEOUT);

            con.setDoOutput(true);
            con.setDoInput(true);
            con.setInstanceFollowRedirects(false);
            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type",
                    "application/json");

            //set cookies
            if (msCookieManager.getCookieStore().getCookies().size() > 0) {
                //While joining the Cookies, use ',' or ';' as needed. Most of the server are using ';'
                con.setRequestProperty(COOKIE ,
                        TextUtils.join(";", msCookieManager.getCookieStore().getCookies()));
            }

            con.setConnectTimeout(10000);
            DataOutputStream dataOutputStream = new DataOutputStream(
                    con.getOutputStream());
            dataOutputStream.write(postData.toString().getBytes("UTF-8"));
            dataOutputStream.flush();
            dataOutputStream.close();

            //Get cookies from response
            Map<String, List<String>> headerFields = con.getHeaderFields();
            List<String> cookiesHeader = headerFields.get(COOKIES_HEADER);

            if (cookiesHeader != null) {
                for (String cookie : cookiesHeader) {
                    msCookieManager.getCookieStore().add(null, HttpCookie.parse(cookie).get(0));
                }
            }

            int status = con.getResponseCode();
            Log.i("HTTP", "Response " + String.valueOf(status));
            if (status == HttpURLConnection.HTTP_OK) {
                InputStream responseStream = new BufferedInputStream(
                        con.getInputStream());
                BufferedReader responseStreamReader = new BufferedReader(
                        new InputStreamReader(responseStream));
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = responseStreamReader.readLine()) != null) {
                    sb.append(line);
                }

                JSONObject obj = new JSONObject(sb.toString());

                Log.i("JSON", obj.toString());
                if (obj.has("status")) {
                    return obj;
                } else {
                    Log.e("httpCOM", "No status tag in response");
                    JSONObject res = new JSONObject();
                    res.put("status", false);
                    return res;
                }
            }
            Log.e("httpCOM", "Response: " + String.valueOf(con.getResponseCode()));
            JSONObject res = new JSONObject();
            res.put("status", false);
            return res;

        } catch (Exception e) {
            e.printStackTrace();
            JSONObject res = new JSONObject();
            try {
                res.put("status", false);
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

    public static JSONObject getSurvey(String id) {


        BufferedReader reader = null;
        HttpURLConnection con = null;


        try {
            URL url = new URL(BASEURL + "getsurvey/" + id);
            Log.i("URL",url.toString());
            con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("GET");

            //Set timeout
            con.setConnectTimeout(CONNECTTIMEOUT);
            con.setReadTimeout(SOCKETTIMEOUT);

            //set cookies
            if (msCookieManager.getCookieStore().getCookies().size() > 0) {
                //While joining the Cookies, use ',' or ';' as needed. Most of the server are using ';'
                con.setRequestProperty(COOKIE ,
                        TextUtils.join(";", msCookieManager.getCookieStore().getCookies()));
            }

            StringBuilder sb = new StringBuilder();
            reader = new BufferedReader((new InputStreamReader(con.getInputStream())));

            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line);
            }
            JSONObject obj = new JSONObject(sb.toString());

            //Get cookies from response
            Map<String, List<String>> headerFields = con.getHeaderFields();
            List<String> cookiesHeader = headerFields.get(COOKIES_HEADER);

            if (cookiesHeader != null) {
                for (String cookie : cookiesHeader) {
                    msCookieManager.getCookieStore().add(null, HttpCookie.parse(cookie).get(0));
                }
            }

            if (obj.has("questions")) {
                Log.e("httpCom", "Retrieving Questions success");
                return obj; 
            } else {
                Log.e("httpCom", "Retrieving Questions failed");
                Log.e("httpCom", "HTTP Request Code: "+ String.valueOf(con.getResponseCode()));
                return null;
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
    
    public static Bitmap getImage(String link) {
        BufferedReader reader = null;
        HttpURLConnection con = null;
       
        Bitmap bitmap;
        
        //Grab image from server
        try {    
            URL url = new URL(BASEURL + "surveyimages/" + link);
            Log.i("URL",url.toString());
            con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("GET");

            //Set timeout
            con.setConnectTimeout(CONNECTTIMEOUT);
            con.setReadTimeout(SOCKETTIMEOUT);

            InputStream in = con.getInputStream();
            bitmap = BitmapFactory.decodeStream(in);
            in.close();
        }
        catch (Exception e) {
            e.printStackTrace();
            try {
                int status = con.getResponseCode();
                Log.e("Retieve Images","Unable to get image: "+String.valueOf(status));
            } catch (IOException e1) {
                e1.printStackTrace();
            }
            bitmap = null;
        }
        return bitmap;
    }
}



