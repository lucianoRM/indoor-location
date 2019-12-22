package com.example.location.activity;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;

import com.example.location.api.system.LocationSystem;
import com.example.location.api.system.SystemConfiguration;

import static android.net.Uri.parse;
import static com.example.location.Utils.showError;
import static com.example.location.activity.SettingsActivity.getSystemConfig;

public abstract class ConnectedActivity extends AppCompatActivity {

    protected SystemConfiguration systemConfiguration;
    protected LocationSystem locationSystem;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.systemConfiguration = getSystemConfig(getApplicationContext());
        this.locationSystem = new LocationSystem(systemConfiguration);
    }

    protected void terminate(String error) {
        Intent data = new Intent();
        data.setData(parse(error));
        setResult(1, data);
        finish();
    }
}
