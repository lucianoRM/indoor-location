package com.example.location.api.entity.sensor;

import java.util.List;

public class DefaultSensorImplementation implements Sensor {

    private SensorFeed sensorFeed;

    public DefaultSensorImplementation(SensorConfiguration config) {
        this.sensorFeed = config.getSensorFeed();
    }

    @Override
    public void sense() {
        List<SensedObject> sensedObjects = sensorFeed.getSensedObjects();
        //

    }
}
