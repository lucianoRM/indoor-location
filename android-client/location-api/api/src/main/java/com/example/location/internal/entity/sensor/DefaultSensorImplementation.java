package com.example.location.internal.entity.sensor;

import com.example.location.api.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.entity.sensor.SensorFeed;

import java.util.List;

public class DefaultSensorImplementation implements Sensor {

    private String id;
    private String name;
    private SensorFeed sensorFeed;

    public DefaultSensorImplementation(SensorConfiguration config) {
        this.id = config.getSensorId();
        this.name = config.getSensorName();
        this.sensorFeed = config.getSensorFeed();
    }

    @Override
    public void sense() {
        List<SensedObject> sensedObjects = sensorFeed.getSensedObjects();
        //

    }

    @Override
    public String getId() {
        return this.id;
    }

    @Override
    public String getName() {
        return this.name;
    }
}
