package com.example.location.api.data;

import com.example.location.api.entity.emitter.SignalEmitter;

/**
 * Transform raw sensed data into distance based data.
 */
@FunctionalInterface
public interface DataTransformer {

    /**
     * Transform raw data from the sensor into usable data for the System
     * @param signalEmitter the emitter source of this data
     * @param rawData the data received by the sensor
     * @return the transformed data.
     */
    SensorData transform(SignalEmitter signalEmitter, RawSensorData rawData);

}
