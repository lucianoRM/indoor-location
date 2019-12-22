package com.example.location.task;

import android.os.AsyncTask;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.system.SensorManager;
import com.example.location.api.system.SensorManagerException;

import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeoutException;

import static java.util.concurrent.TimeUnit.MILLISECONDS;

public final class CreateSensorAsyncTask extends AsyncTask<SensorConfiguration, Void, Sensor> {

    //TODO:Make this configurable
    private static final long DEFAULT_TIMEOUT_MILLIS = 5000;

    private SensorManager sensorManager;

    public static Sensor createSensor(SensorManager sensorManager, SensorConfiguration sensorConfiguration) throws AsyncTaskException {
        AsyncTask<SensorConfiguration, Void, Sensor> createSensor = new CreateSensorAsyncTask(sensorManager).execute(sensorConfiguration);
        try {
            return createSensor.get(DEFAULT_TIMEOUT_MILLIS, MILLISECONDS);
        } catch (InterruptedException | ExecutionException | TimeoutException e) {
            throw new AsyncTaskException(e);
        }
    }

    private CreateSensorAsyncTask(SensorManager sensorManager) {
        this.sensorManager = sensorManager;
    }

    @Override
    protected Sensor doInBackground(SensorConfiguration... sensorConfigurations) {
        try {
            return sensorManager.getOrCreateSensor(sensorConfigurations[0]);
        } catch (SensorManagerException e) {
            throw new RuntimeException(e);
        }
    }
}
