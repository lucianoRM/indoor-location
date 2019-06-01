package com.example.location.internal.client;

import com.example.location.api.client.SensorLocationClient;
import com.example.location.api.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.internal.http.LocationService;

import java.util.List;

import javax.inject.Inject;

public class DefaultSensorLocationClient implements SensorLocationClient {

    private LocationService locationService;

    @Inject
    public DefaultSensorLocationClient(LocationService locationService) {
        this.locationService = locationService;
    }

    @Override
    public void onNewSensedObjects(Sensor sensor, List<SensedObject> sensedObjects) {

    }


}
