package com.example.location.api.system;

/**
 * Exception thrown if attempting to register a new {@link com.example.location.api.entity.emitter.SignalEmitter} and it already exists
 */
public class EmitterAlreadyExistsException extends EmitterManagerException {

    public EmitterAlreadyExistsException(String message) {
        super(message);
    }

    public EmitterAlreadyExistsException(String message, Throwable e) {
        super(message, e);
    }
}
