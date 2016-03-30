package com.blank_canvas.nathan_pc.location_alarm;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/**
 * Created by Nathan on 30/03/2016.
 */
public class AlarmReceiver extends BroadcastReceiver {
    public static final int REQUEST_CODE = 12345;

    // when broadcast message is received start service (CheckLocation class)
    @Override
    public void onReceive(Context context, Intent intent) {
        Intent i = new Intent(context, CheckLocation.class);
        context.startService(i);
    }
}
