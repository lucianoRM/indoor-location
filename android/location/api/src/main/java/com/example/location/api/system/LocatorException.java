package com.example.location.api.system;

import com.example.location.internal.entity.User;

/**
 * Exception thrown when there is an error locating the {@link User}
 */
public class LocatorException extends Exception {

    public LocatorException(String message) {
        super(message);
    }

    public LocatorException(String message, Throwable cause) {
        super(message, cause);
    }

    public LocatorException(Throwable cause) {
        super(cause);
    }
}
