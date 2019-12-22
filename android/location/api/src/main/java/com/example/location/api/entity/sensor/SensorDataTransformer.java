package com.example.location.api.entity.sensor;

import com.example.location.api.data.RawSensorData;
import com.example.location.api.data.SensorData;

/**
 * Transform raw sensed data into distance based data.
 */
@FunctionalInterface
public interface SensorDataTransformer {

    /**
     * Transform raw data from the sensor into usable data for the LocationSystem
     * @param rawData the data received by the sensor
     * @param context context with available information to compute data correctly
     * @return the transformed data.
     */
    SensorData transform(RawSensorData rawData, SensorContext context);

}
