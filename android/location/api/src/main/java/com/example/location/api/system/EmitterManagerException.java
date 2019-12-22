package com.example.location.api.system;

/**
 * Root exception thrown by a {@link EmitterManager}
 */
public class EmitterManagerException extends Exception {

    public EmitterManagerException(String message) {
        super(message);
    }

    public EmitterManagerException(String message, Throwable e) {
        super(message, e);
    }

}
