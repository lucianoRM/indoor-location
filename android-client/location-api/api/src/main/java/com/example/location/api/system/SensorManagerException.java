package com.example.location.api.system;

/**
 * Exception raised by a {@link SensorManager}.
 */
public class SensorManagerException extends Exception {

    public SensorManagerException(String message) {
        super(message);
    }

    public SensorManagerException(String message, Throwable cause) {
        super(message, cause);
    }
}
