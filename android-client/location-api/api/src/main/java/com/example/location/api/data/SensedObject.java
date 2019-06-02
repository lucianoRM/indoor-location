package com.example.location.api.data;

public class SensedObject {

    private String id;
    private RawSensorData data;

    public SensedObject(String id, RawSensorData sensorData) {
        this.id = id;
        this.data = sensorData;
    }

    public String getId() {
        return id;
    }

    public RawSensorData getRawData() {
        return data;
    }
}
