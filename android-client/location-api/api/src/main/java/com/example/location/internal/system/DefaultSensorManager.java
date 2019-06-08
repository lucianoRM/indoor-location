package com.example.location.internal.system;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.system.EmitterManager;
import com.example.location.api.system.SensorManager;
import com.example.location.internal.entity.sensor.DefaultSensor;
import com.example.location.functional.http.HttpLocationClient;
import com.example.location.functional.http.HttpSensorListener;

import java.io.IOException;

import javax.inject.Inject;

import retrofit2.Call;
import retrofit2.Response;

public class DefaultSensorManager implements SensorManager {

    private HttpLocationClient httpLocationClient;
    private EmitterManager emitterManager;

    @Inject
    public DefaultSensorManager(HttpLocationClient httpLocationClient,
                                EmitterManager emitterManager) {
        this.httpLocationClient = httpLocationClient;
        this.emitterManager = emitterManager;
    }

    @Override
    public Sensor createSensor(SensorConfiguration config) {
        final Sensor sensor =
                new DefaultSensor(
                        config.getSensorId(),
                        config.getSensorName(),
                        config.getSensorFeed(),
                        config.getDataTransformer(),
                        new HttpSensorListener(httpLocationClient),
                        emitterManager
                );

        Call<Sensor> httpCall = httpLocationClient.registerSensor(sensor);
        try {
            Response<Sensor> httpResponse = httpCall.execute();
        }catch (IOException e) {
            //TODO: wrap this
            throw new RuntimeException(e);
        }
        return sensor;
    }
}
