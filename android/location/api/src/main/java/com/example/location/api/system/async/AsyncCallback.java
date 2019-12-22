package com.example.location.api.system.async;

import com.example.location.internal.async.DefaultAsyncCallback;

import java.util.function.Consumer;

/**
 * Callback to be executed after completing an async operation
 */
public interface AsyncCallback<T> {

    /**
     * Provide a simple callback construction
     * @param onSuccess to be executed on success
     * @param onFailure to be executed on failure
     * @param <Y> the type processed by the callbacks
     * @return a simple {@link AsyncCallback<Y>}
     */
    static <Y> AsyncCallback<Y> newCallback(Consumer<AsyncOpSuccess<Y>> onSuccess, Consumer<AsyncOpFailure> onFailure) {
        return new DefaultAsyncCallback<>(onSuccess, onFailure);
    }

    /**
     * Method executed when the operation finished successfully
     * @param success information about the executed operation
     */
    void onSuccess(AsyncOpSuccess<T> success);

    /**
     * Method executed after the operation failed
     * @param failure information about the failed operation
     */
    void onFailure(AsyncOpFailure failure);

}
