package com.example.location.internal.client;

import com.example.location.internal.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.internal.http.HttpLocationClient;

import java.util.List;

import javax.inject.Inject;

public class DefaultSensorLocationClient implements SensorLocationClient {

    private HttpLocationClient httpLocationClient;

    @Inject
    public DefaultSensorLocationClient(HttpLocationClient httpLocationClient) {
        this.httpLocationClient = httpLocationClient;
    }

    @Override
    public void onNewSensedObjects(Sensor sensor, List<SensedObject> sensedObjects) {

    }


}
