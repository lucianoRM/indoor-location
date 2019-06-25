package com.example.luciano.location;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.TextView;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    private Map<String, Class> accesibleActivities;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        this.accesibleActivities = new HashMap<>();
        this.accesibleActivities.put("WIFI_VIEW", WifiSignalViewActivity.class);
        this.accesibleActivities.put("SENSOR_VIEW", SensorActivity.class);

        RecyclerView recyclerView = findViewById(R.id.availableActivitiesRecyclerView);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(new AvailableActivitiesAdapter(accesibleActivities.keySet()));
    }

    public void startActivity(View view) {
        TextView activityView = view.findViewById(R.id.activityName);
        String activityName = activityView.getText().toString();
        Intent intent = new Intent(this, accesibleActivities.get(activityName));
        startActivity(intent);
    }
}
