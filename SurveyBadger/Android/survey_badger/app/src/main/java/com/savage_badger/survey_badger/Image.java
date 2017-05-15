package com.savage_badger.survey_badger;

import android.graphics.Bitmap;

public class Image {
    Bitmap bitmap;
    String value;
    
    public Image() {
        this.bitmap = null;
        this.value = "";
    }

    public Image(Bitmap bitmap, String value) {
        this.bitmap = bitmap;
        this.value= value;
    }


    public Bitmap getBitmap() {
        return this.bitmap;
    }

    public void setBitmap(Bitmap bitmap) {
        this.bitmap = bitmap;
    }
    
    public String getValue() {
        return this.value;
    }

    public void setValue(String value) {
        this.value = value;
    }

}
