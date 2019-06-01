package com.example.location.api.entity.sensor;

import com.example.location.api.data.SensedObject;

import java.util.List;

/**
 * Interacts with any external system and retrieves the actual values being sensed.
 */
public interface SensorFeed {

    /**
     * Collect the last sensed objects
     * @return a {@link List<SensedObject>} with the objects sensed
     */
    List<SensedObject> getSensedObjects();
}
