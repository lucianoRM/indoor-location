package com.example.location;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.support.v7.app.AlertDialog;

import com.example.location.api.system.SystemConfiguration;

import java.util.Optional;
import java.util.concurrent.Callable;

import okhttp3.Response;

import static java.lang.String.format;
import static java.util.concurrent.TimeUnit.MILLISECONDS;

public class Utils {

    public static void showError(String error, Context context) {
        AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(context);
        alertDialogBuilder.setMessage(error);
        alertDialogBuilder.setCancelable(true);

        alertDialogBuilder.setPositiveButton(
                "Close",
                (dialog, id) -> dialog.cancel());

        AlertDialog alert = alertDialogBuilder.create();
        alert.show();
    }

}
