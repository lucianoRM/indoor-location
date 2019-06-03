package com.example.location.api.entity.sensor;

import com.example.location.api.data.RawSensorData;
import com.example.location.internal.data.SensedObject;

import java.util.List;

/**
 * Interacts with any external system and retrieves the actual values being sensed.
 */
public interface SensorFeed {

    /**
     * Collect the last sensed objects data
     * @return a {@link List<RawSensorData>} with the data from the objects sensed
     */
    List<RawSensorData> getData();
}
