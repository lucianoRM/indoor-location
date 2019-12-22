package com.example.location.api.system.async;

/**
 * Information to send after an async operation failed
 */
public interface AsyncOpFailure {

    /**
     * @return a message with the failure description
     */
    String errorMessage();

}
