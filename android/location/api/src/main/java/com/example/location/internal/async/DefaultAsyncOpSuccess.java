package com.example.location.internal.async;

import com.example.location.api.system.async.AsyncOpSuccess;

public class DefaultAsyncOpSuccess<T> implements AsyncOpSuccess<T> {

    private T result;

    public DefaultAsyncOpSuccess(T result) {
        this.result = result;
    }

    @Override
    public T getResult() {
        return result;
    }
}
