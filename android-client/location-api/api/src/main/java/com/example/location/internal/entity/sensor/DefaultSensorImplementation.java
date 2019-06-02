package com.example.location.internal.entity.sensor;

import com.example.location.api.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorFeed;

import java.util.List;

public class DefaultSensorImplementation implements Sensor {

    private String id;
    private String name;
    private SensorFeed feed;
    private SensorListener listener;

    public DefaultSensorImplementation(String id, String name, SensorFeed feed, SensorListener listener) {
        this.id = id;
        this.name = name;
        this.feed = feed;
        this.listener = listener;
    }

    @Override
    public void sense() {
        List<SensedObject> sensedObjects = feed.getSensedObjects();
        listener.onSensorUpdate(this, sensedObjects);
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
