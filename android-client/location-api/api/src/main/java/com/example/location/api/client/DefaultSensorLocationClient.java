package com.example.location.api.client;

import com.example.location.api.entity.sensor.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.http.LocationService;

import java.util.List;

import javax.inject.Inject;

public class DefaultSensorLocationClient implements SensorLocationClient {

    @Inject
    private LocationService locationService;

    @Override
    public void onNewSensedObjects(Sensor sensor, List<SensedObject> sensedObjects) {

    }


}
