package com.blank_canvas.nathan_pc.location_alarm;

import android.Manifest;
import android.app.IntentService;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationServices;

import java.io.IOException;
import java.util.List;
import java.util.Locale;

/**
 * Created by Nathan on 30/03/2016.
 */
public class CheckLocation extends IntentService implements GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener {

    public static String suburb;
    private GoogleApiClient mGoogleApiClient;
    private Location lastLocation;
    private Geocoder geocoder;
    List<Address> addresses;

    /**
     * Creates an IntentService.  Invoked by your subclass's constructor.
     *
     * @param //name Used to name the worker thread, important only for debugging.
     */

    // android studio wants this
    public CheckLocation() {
        super("CheckLocation");
    }

    // and it wants this
    public CheckLocation(String name) {
        super(name);
    }

    public static void setSuburb(String name) {
        suburb = name;
    }

    public static String getSuburb() {
        return suburb;
    }

    // when the service is started, it goes here
    @Override
    protected void onHandleIntent(Intent intent) {
        if (mGoogleApiClient == null) {
            mGoogleApiClient = new GoogleApiClient.Builder(this)
                    .addConnectionCallbacks(this)
                    .addOnConnectionFailedListener(this)
                    .addApi(LocationServices.API)
                    .build();
        }

        mGoogleApiClient.connect();
    }

    // called after connect()
    @Override
    public void onConnected(Bundle bundle) {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // not used but needed, there is a check for this in the MainActivity
            return;
        }

        lastLocation = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient); // gets the last location on the phone

        geocoder = new Geocoder(this, Locale.getDefault());

        try {
            addresses = geocoder.getFromLocation(lastLocation.getLatitude(), lastLocation.getLongitude(), 1);
        } catch (IOException e) {
            e.printStackTrace();
        }

        // if the current suburb is the set suburb then start AlarmActivity class
        if (addresses.get(0).getLocality().equals(suburb)) {
            Intent i = new Intent(getBaseContext(), AlarmActivity.class);
            i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            getApplication().startActivity(i);
        }
    }

    @Override
    public void onConnectionSuspended(int i) {

    }

    @Override
    public void onConnectionFailed(ConnectionResult connectionResult) {

    }
}
