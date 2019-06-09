package com.example.location.api.system;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;

/**
 * Handles {@link Sensor}s.
 */
public interface SensorManager {

    /**
     * Create a new {@link Sensor} and register it in the system
     * @param config The sensor configuration to be created
     * @return The new Sensor being created
     */
    Sensor createSensor(SensorConfiguration config) throws SensorManagerException;

}
