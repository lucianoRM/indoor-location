package com.example.location.internal.http;

import com.example.location.api.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.internal.entity.sensor.SensorListener;

import java.util.List;

/**
 * {@link SensorListener} that connects to a remote HttpServer when the {@link com.example.location.api.entity.sensor.Sensor} updates it's sensed objects
 */
public class HttpSensorListener implements SensorListener {

    private LocationService locationService;

    public HttpSensorListener(LocationService locationService) {
        this.locationService = locationService;
    }

    @Override
    public void onSensorUpdate(Sensor sensor, List<SensedObject> sensedObjects) {
        locationService.getSignalEmitters();
        System.out.println("SENSOR: " + sensor + " objects: " + sensedObjects);
    }
}
