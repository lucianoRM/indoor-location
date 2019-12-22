package com.example.location.api.system.async;

/**
 * Information sent after an async operation was successful
 */
public interface AsyncOpSuccess<T> {

    /**
     * Get the result of executing the operation
     * @return the result of executing the operation.
     */
    T getResult();

}
