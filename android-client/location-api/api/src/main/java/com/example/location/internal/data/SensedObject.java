package com.example.location.internal.data;

import com.example.location.api.data.SensorData;

public class SensedObject {

    private String id;
    private SensorData data;

    public SensedObject(String id, SensorData sensorData) {
        this.id = id;
        this.data = sensorData;
    }

    public String getId() {
        return id;
    }

    public SensorData getData() {
        return data;
    }
}
