package com.example.location.activity;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.TextView;

import com.example.location.adapter.AvailableActivitiesAdapter;
import com.example.location.R;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import static com.example.location.Utils.showError;

public class MainActivity extends AppCompatActivity {

    public static final String LOG_TAG = "INDOOR_LOCATION";
    private Map<String, Class> accesibleActivities;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        this.accesibleActivities = new HashMap<>();
        this.accesibleActivities.put("WIFI_VIEW", WifiSignalViewActivity.class);
        this.accesibleActivities.put("BLUETOOTH VIEW", BleViewActivity.class);
        this.accesibleActivities.put("USER POSITION VIEW", UserPositionActivity.class);
        this.accesibleActivities.put("CONFIGURE SERVER", ServerUpdateActivity.class);
        this.accesibleActivities.put("SETTINGS", SettingsActivity.class);
        this.accesibleActivities.put("CALIBRATE BLE", BleCalibrationActivity.class);
        this.accesibleActivities.put("MEASUREMENTS", MeasurementsActivity.class);

        RecyclerView recyclerView = findViewById(R.id.availableActivitiesRecyclerView);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(new AvailableActivitiesAdapter(new ArrayList<>(accesibleActivities.keySet())));
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        if(resultCode != 0) {
            showError(data.getDataString(), MainActivity.this);
        }
    }

    public void startActivity(View view) {
        TextView activityView = view.findViewById(R.id.activityName);
        String activityName = activityView.getText().toString();
        Intent intent = new Intent(this, accesibleActivities.get(activityName));
        startActivityForResult(intent, 0);
    }
}
