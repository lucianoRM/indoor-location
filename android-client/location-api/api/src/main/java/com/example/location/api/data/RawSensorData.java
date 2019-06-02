package com.example.location.api.data;

/**
 * Raw data sensed by the sensor corresponding to one {@link com.example.location.api.entity.emitter.SignalEmitter}
 */
public class RawSensorData {

    private float signalValue;
    private long timestamp;

    public RawSensorData(float signalValue, long timestamp) {
        this.signalValue = signalValue;
        this.timestamp = timestamp;
    }

    public float getSignalValue() {
        return signalValue;
    }

    public long getTimestamp() {
        return timestamp;
    }
}
