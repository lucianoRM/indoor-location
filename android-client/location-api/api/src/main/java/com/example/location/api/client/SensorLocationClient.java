package com.example.location.api.client;

import com.example.location.api.entity.sensor.SensedObject;
import com.example.location.api.entity.sensor.Sensor;

import java.util.List;

/**
 * A {@link LocationClient} that will interact with the Location Server.
 */
public interface SensorLocationClient extends LocationClient {

    /**
     * Notify the {@link SensorLocationClient} that new data was sensed.
     * @param sensor The {@link Sensor} that sensed these new objects
     * @param sensedObjects the new objects received by the {@param sensor}.
     */
    void onNewSensedObjects(Sensor sensor, List<SensedObject> sensedObjects);

}
