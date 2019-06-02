package com.example.location.internal.entity.sensor;

import com.example.location.api.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;

import java.util.List;

/**
 * Listens to {@link com.example.location.api.entity.sensor.Sensor}s and executes an action when they update their information.
 */
public interface SensorListener {

    /**
     * Executes an action when the sensor updates it's objects
     * @param sensor the sensor being listened
     * @param sensedObjects the new objects sensed by the sensor
     */
    void onSensorUpdate(Sensor sensor, List<SensedObject> sensedObjects);

}
