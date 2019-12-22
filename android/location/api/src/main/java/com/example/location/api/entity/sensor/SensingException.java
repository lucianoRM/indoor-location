package com.example.location.api.entity.sensor;

/**
 * {@link Exception} thrown if there is an error while executing a {@link Sensor} sensing action.
 */
public class SensingException extends Exception {

    public SensingException(String message) {
        super(message);
    }

    public SensingException(String message, Throwable cause) {
        super(message + cause.getMessage(), cause);
    }

    public SensingException(Throwable cause) {
        super(cause);
    }
}
