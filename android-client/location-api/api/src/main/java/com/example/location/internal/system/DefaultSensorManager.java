package com.example.location.internal.system;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.system.SensorManager;
import com.example.location.internal.entity.sensor.DefaultSensor;
import com.example.location.internal.http.HttpLocationClient;
import com.example.location.internal.http.HttpSensorListener;

import javax.inject.Inject;

public class DefaultSensorManager implements SensorManager {

    private HttpLocationClient httpLocationClient;

    @Inject
    public DefaultSensorManager(HttpLocationClient httpLocationClient) {
        this.httpLocationClient = httpLocationClient;
    }

    @Override
    public Sensor createSensor(SensorConfiguration config) {
        return new DefaultSensor(
                config.getSensorId(),
                config.getSensorName(),
                config.getSensorFeed(),
                config.getDataTransformer(),
                new HttpSensorListener(httpLocationClient)
        );
    }
}
