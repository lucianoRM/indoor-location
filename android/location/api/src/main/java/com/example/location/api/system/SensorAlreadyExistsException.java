package com.example.location.api.system;

/**
 * Exception thrown when the sensor being registered already exists
 */
public class SensorAlreadyExistsException extends SensorManagerException {

    public SensorAlreadyExistsException(String message) {
        super(message);
    }

    public SensorAlreadyExistsException(String message, Throwable cause) {
        super(message, cause);
    }
}
