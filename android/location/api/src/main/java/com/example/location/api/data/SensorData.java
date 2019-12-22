package com.example.location.api.data;

/**
 * Data sensed by the sensor corresponding to one {@link com.example.location.api.entity.emitter.SignalEmitter}
 */
public class SensorData {

    private float distance;
    private long timestamp;

    public SensorData(float distance, long timestamp) {
        this.distance = distance;
        this.timestamp = timestamp;
    }

    public float getDistance() {
        return distance;
    }

    public long getTimestamp() {
        return timestamp;
    }
}
