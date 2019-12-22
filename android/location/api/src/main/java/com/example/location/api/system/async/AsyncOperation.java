package com.example.location.api.system.async;

/**
 * {@link FunctionalInterface} for an operation to be executed asynchronously. To notify failure, it should
 * raise an exception.
 * @param <T> return type
 */
@FunctionalInterface
public interface AsyncOperation<T> {

    /**
     * Execute the operation
     * @return the result
     * @throws Exception
     */
    T execute() throws Exception;

}

