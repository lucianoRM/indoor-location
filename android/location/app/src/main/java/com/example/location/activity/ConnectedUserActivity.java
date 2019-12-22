package com.example.location.activity;

import android.os.Bundle;

import com.example.location.task.AsyncTaskException;

import java.io.IOException;

import okhttp3.Response;

import static com.example.location.task.HttpUtils.registerUser;

/**
 * Activity that works only when there is a connection from this user to the Location system
 */
public abstract class ConnectedUserActivity extends ConnectedActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //REGISTER USER or CHECK IF ALREADY EXISTS
        try {
            Response response = registerUser(systemConfiguration);
            if (!response.isSuccessful() && response.code() != 409) {
                terminate(response.body().string());
            }
        } catch (AsyncTaskException | IOException e) {
            terminate(e.getMessage());
        }
    }
}
