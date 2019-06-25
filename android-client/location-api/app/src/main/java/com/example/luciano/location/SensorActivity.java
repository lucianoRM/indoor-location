package com.example.luciano.location;

import android.graphics.Color;
import android.net.wifi.WifiManager;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.system.LocationSystem;
import com.example.location.api.system.SensorManager;
import com.example.location.api.system.SensorManagerException;
import com.example.location.impl.wifi.WiFiSensorFeed;
import com.example.location.impl.wifi.WifiTransformer;

import java.util.concurrent.TimeUnit;

import static android.graphics.Color.GRAY;
import static android.graphics.Color.GREEN;
import static android.graphics.Color.RED;
import static android.util.Log.getStackTraceString;
import static com.example.location.api.entity.sensor.SensorConfiguration.sensorConfigurationBuilder;
import static java.util.concurrent.TimeUnit.MILLISECONDS;

public class SensorActivity extends AppCompatActivity {

    private WifiManager wifiManager;
    private Sensor sensor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sensor);

        this.wifiManager = (WifiManager) getSystemService(WIFI_SERVICE);

        LocationSystem locationSystem = new LocationSystem();
        SensorManager sensorManager = locationSystem.getSensorManager();
        CreateSensorAsyncTask createSensorAsyncTask = new CreateSensorAsyncTask(sensorManager);

        createSensorAsyncTask.execute(sensorConfigurationBuilder()
                .withId("android_sensor")
                .withFeed(new WiFiSensorFeed(getApplicationContext()))
                .withTransformer(new WifiTransformer())
                .build());
        try {
            sensor = createSensorAsyncTask.get(1000, MILLISECONDS);
        }catch (Exception e) {
            Log.e("location", getStackTraceString(e));
        }
    }


    private static final class SenseAsyncTask extends AsyncTask<Sensor, Void, Void> {

        @Override
        protected Void doInBackground(Sensor... sensors) {
            sensors[0].sense();
            return null;
        }
    }

    private static final class CreateSensorAsyncTask extends AsyncTask<SensorConfiguration,Void,Sensor> {

        private SensorManager sensorManager;

        public CreateSensorAsyncTask(SensorManager sensorManager) {
            this.sensorManager = sensorManager;
        }

        @Override
        protected Sensor doInBackground(SensorConfiguration... sensorConfigurations) {
            try {
                return sensorManager.createSensor(sensorConfigurations[0]);
            }catch (SensorManagerException e) {
                throw new RuntimeException(e);
            }
        }
    }

    public void sense(View view) {
        Button senseButton = view.findViewById(R.id.sense);
        senseButton.setBackgroundColor(GRAY);

        SenseAsyncTask senseAsyncTask = new SenseAsyncTask();
        if(sensor != null) {
            senseAsyncTask.execute(sensor);
        }
        try {
            senseAsyncTask.get(1000, MILLISECONDS);
            senseButton.setBackgroundColor(GREEN);
        }catch (Exception e) {
            senseButton.setBackgroundColor(RED);
            Log.e("location", getStackTraceString(e));
        }
    }

}
