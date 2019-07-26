package com.example.luciano.location;

import android.net.wifi.WifiManager;
import android.os.AsyncTask;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.example.location.api.data.Position;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.system.LocationSystem;
import com.example.location.api.system.Locator;
import com.example.location.api.system.SensorManager;
import com.example.location.api.system.SensorManagerException;
import com.example.location.impl.wifi.WiFiSensorFeed;
import com.example.location.impl.wifi.WifiTransformer;

import static android.graphics.Color.GRAY;
import static android.graphics.Color.GREEN;
import static android.graphics.Color.RED;
import static android.util.Log.getStackTraceString;
import static com.example.location.api.entity.sensor.SensorConfiguration.sensorConfigurationBuilder;
import static java.lang.String.format;
import static java.util.concurrent.TimeUnit.MILLISECONDS;

public class UserPositionActivity extends AppCompatActivity {

    private WifiManager wifiManager;
    private Sensor sensor;
    private String userId;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        this.userId = "USER";
        setContentView(R.layout.user_position);

        this.wifiManager = (WifiManager) getSystemService(WIFI_SERVICE);

        LocationSystem locationSystem = new LocationSystem(userId, "192.168.1.5", 8082);
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
            finish();
        }

        Handler handler = new Handler();
        final Runnable runnableCode = new Runnable() {
            @Override
            public void run() {
                GetPositionAsyncTask getPositionAsyncTask = new GetPositionAsyncTask(locationSystem.getLocator());
                Position position;
                try {
                    getPositionAsyncTask.execute();
                    position = getPositionAsyncTask.get(1000, MILLISECONDS);
                    updatePosition(format("%.1f",position.getX()), format("%.1f",position.getY()));
                }catch (Exception e) {
                    Log.e("location", getStackTraceString(e));
                }
                handler.postDelayed(this, 1000);
            }
        };
        handler.post(runnableCode);

        Handler handler2 = new Handler();
        final Runnable runnableCode2 = new Runnable() {
            @Override
            public void run() {
                wifiManager.startScan();
                handler2.postDelayed(this, 15000);
            }
        };
        handler2.post(runnableCode2);
    }

    public void updatePosition(String newX, String newY) {
       TextView x = findViewById(R.id.xValueTextView);
       TextView y = findViewById(R.id.yValueTextView);
       x.setText(newX);
       y.setText(newY);
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
                return sensorManager.getOrCreateSensor(sensorConfigurations[0].getSensorId(), sensorConfigurations[0]);
            }catch (SensorManagerException e) {
                throw new RuntimeException(e);
            }
        }
    }

    private static final class GetPositionAsyncTask extends AsyncTask<Void, Void, Position> {

        private Locator locator;

        public GetPositionAsyncTask(Locator locator) {
            this.locator = locator;
        }

        @Override
        protected Position doInBackground(Void... voids) {
            return locator.getPosition();
        }
    }
}
