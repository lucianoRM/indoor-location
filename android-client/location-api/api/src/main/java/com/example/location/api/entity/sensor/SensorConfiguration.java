package com.example.location.api.entity.sensor;

public class SensorConfiguration {

    private SensorFeed sensorFeed;

    public SensorConfiguration(SensorFeed sensorFeed) {
        this.sensorFeed = sensorFeed;
    }

    public SensorFeed getSensorFeed() {
        return sensorFeed;
    }
}
