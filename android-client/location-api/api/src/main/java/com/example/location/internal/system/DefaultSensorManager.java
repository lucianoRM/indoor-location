package com.example.location.internal.system;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.system.SensorManager;

import javax.inject.Inject;

public class DefaultSensorManager implements SensorManager {

    @Inject
    public DefaultSensorManager() {}

    @Override
    public Sensor createSensor(SensorConfiguration config) {
        return null;
    }
}
