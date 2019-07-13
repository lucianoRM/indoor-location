package com.example.location.api.system;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;

/**
 * Handles {@link Sensor}s.
 */
public interface SensorManager {

    /**
     * Try to get a sensor with the given id. If it does not exists,
     * create a new {@link Sensor} using the given and register it in the system
     * @param config The sensor configuration to be created
     * @return The new Sensor being created
     */
    Sensor getOrCreateSensor(String sensorId, SensorConfiguration config) throws SensorManagerException;

    /**
     * Create a new {@link Sensor} and register it in the system.
     * If the sensor already exists, throw an exception.
     * @param config The sensor configuration to be created
     * @return The new Sensor being created
     */
    Sensor createSensor(SensorConfiguration config) throws SensorManagerException;

}
