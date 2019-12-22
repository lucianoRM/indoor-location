package com.example.location.internal.async;

import com.example.location.api.system.async.AsyncCallback;
import com.example.location.api.system.async.AsyncOpFailure;
import com.example.location.api.system.async.AsyncOpSuccess;

import java.util.function.Consumer;

public class DefaultAsyncCallback<T> implements AsyncCallback<T> {

    private Consumer<AsyncOpSuccess<T>> onSuccess;
    private Consumer<AsyncOpFailure> onFailure;

    public DefaultAsyncCallback(Consumer<AsyncOpSuccess<T>> onSuccess, Consumer<AsyncOpFailure> onFailure) {
        this.onSuccess = onSuccess;
        this.onFailure = onFailure;
    }

    @Override
    public void onSuccess(AsyncOpSuccess<T> success) {
        onSuccess.accept(success);
    }

    @Override
    public void onFailure(AsyncOpFailure failure) {
        onFailure.accept(failure);
    }
}
