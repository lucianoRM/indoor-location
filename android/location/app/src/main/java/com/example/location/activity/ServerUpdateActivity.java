package com.example.location.activity;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.example.location.R;
import com.example.location.task.AsyncTaskException;
import com.example.location.task.HttpUtils;

import java.io.IOException;

import okhttp3.Response;

import static android.graphics.Color.GRAY;
import static android.graphics.Color.GREEN;
import static android.graphics.Color.RED;
import static com.example.location.activity.SettingsActivity.getSystemConfig;
import static com.example.location.Utils.showError;
import static com.example.location.task.HttpUtils.addSignalEmitter;
import static java.lang.Float.parseFloat;
import static java.lang.Integer.parseInt;

public class ServerUpdateActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_server_update);
    }

    public void registerAnchor(View view) {
        Button registerButton = view.findViewById(R.id.anchorRegisterButton);
        String anchorId = ((EditText)findViewById(R.id.registerAnchorIdText)).getText().toString();
        float anchorX = parseFloat(((EditText) findViewById(R.id.registerAnchorXText)).getText().toString());
        float anchorY = parseFloat(((EditText) findViewById(R.id.registerAnchorYText)).getText().toString());
        registerButton.setBackgroundColor(GRAY);
        Response response;
        try {
            response = HttpUtils.registerAnchor(anchorId, anchorX, anchorY, getSystemConfig(this));
            if(response.isSuccessful()) {
                registerButton.setBackgroundColor(GREEN);
            }else {
                showError(response.body().string(), ServerUpdateActivity.this);
                registerButton.setBackgroundColor(RED);
            }
        }catch (AsyncTaskException | IOException e) {
            showError(e.toString(), ServerUpdateActivity.this);
        }
    }

    public void deleteAnchor(View view) {
        Button deleteAnchorButton = view.findViewById(R.id.deleteAnchorButton);
        String anchorId = ((EditText) findViewById(R.id.registerAnchorIdText)).getText().toString();
        deleteAnchorButton.setBackgroundColor(GRAY);
        Response response;
        try {
            response = HttpUtils.deleteAnchor(anchorId, getSystemConfig(this));
            if(response.isSuccessful()) {
                deleteAnchorButton.setBackgroundColor(GREEN);
            }else {
                showError(response.body().string(), ServerUpdateActivity.this);
                deleteAnchorButton.setBackgroundColor(RED);
            }
        }catch (AsyncTaskException | IOException e) {
            showError(e.toString(), ServerUpdateActivity.this);
        }
    }

    public void registerSignalEmitter(View view) {
        Button addSignalEmitter = view.findViewById(R.id.addSignalEmitterButton);
        String anchorId = ((EditText) findViewById(R.id.addSignalEmitterAnchorIdText)).getText().toString();
        String signalEmitterId = ((EditText) findViewById(R.id.addSignalEmitteIdText)).getText().toString();
//        int oneMeterPower = parseInt(((EditText) findViewById(R.id.addSignalEmitterAnchor1MPowerText)).getText().toString());
        int oneMeterPower = -63;
        addSignalEmitter.setBackgroundColor(GRAY);
        Response response;
        try {
            response = addSignalEmitter(anchorId, signalEmitterId, oneMeterPower, getSystemConfig(this));
            if(response.isSuccessful()) {
                addSignalEmitter.setBackgroundColor(GREEN);
            }else {
                showError(response.body().string(), ServerUpdateActivity.this);
                addSignalEmitter.setBackgroundColor(RED);
            }
        }catch (AsyncTaskException | IOException e) {
            showError(e.toString(), ServerUpdateActivity.this);
        }
    }

}
