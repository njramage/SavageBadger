package com.example.nathan.customnumberpicker;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RectF;
import android.view.View;

/**
 * Created by nathan on 15/12/16.
 */

public class Avocado extends View {
    public Avocado(Context context) {
        super(context);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        Paint paint = new Paint();
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(10);
        paint.setColor(Color.GRAY);
        RectF oval = new RectF(10, 600, 600, 1000);
        canvas.drawArc(oval, 30, 120, true, paint);

        canvas.drawLine(47, 900, 100, 600, paint);

        oval = new RectF(10, 30, 200, 700);
        canvas.drawArc(oval, 150, 200, true, paint);
    }
}
