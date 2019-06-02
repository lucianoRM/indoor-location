package com.example.location.internal.system;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.system.SensorManager;
import com.example.location.internal.entity.sensor.DefaultSensorImplementation;
import com.example.location.internal.http.HttpSensorListener;
import com.example.location.internal.http.LocationService;

import javax.inject.Inject;

public class DefaultSensorManager implements SensorManager {

    private LocationService locationService;

    @Inject
    public DefaultSensorManager(LocationService locationService) {
        this.locationService = locationService;
    }

    @Override
    public Sensor createSensor(SensorConfiguration config) {
        return new DefaultSensorImplementation(
                config.getSensorId(),
                config.getSensorName(),
                config.getSensorFeed(),
                new HttpSensorListener(locationService)
        );
    }
}
