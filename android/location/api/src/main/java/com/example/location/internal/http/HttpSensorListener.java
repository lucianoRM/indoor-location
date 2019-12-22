package com.example.location.internal.http;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.internal.data.SensedObject;
import com.example.location.internal.entity.sensor.SensorListener;

import java.io.IOException;
import java.util.List;

import retrofit2.Call;
import retrofit2.Response;

/**
 * {@link SensorListener} that connects to a remote HttpServer when the
 * {@link Sensor} updates it's sensed objects
 */
public class HttpSensorListener implements SensorListener {

    private HttpLocationClient httpLocationClient;

    public HttpSensorListener(HttpLocationClient httpLocationClient) {
        this.httpLocationClient = httpLocationClient;
    }

    @Override
    public void onSensorUpdate(Sensor sensor, List<SensedObject> sensedObjects) {
        Call<String> updateSensorCall = httpLocationClient.updateSensor(sensor.getId(), sensedObjects, null);
        try {
            Response<String> res = updateSensorCall.execute();
            if(!res.isSuccessful()) {
                throw new RuntimeException("Sensor update request unsuccessful " + res.errorBody().string());
            }
        }catch (IOException e) {
            //TODO: fix this
            throw new RuntimeException(e);
        }
    }
}
