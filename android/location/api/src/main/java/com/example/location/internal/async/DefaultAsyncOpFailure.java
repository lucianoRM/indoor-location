package com.example.location.internal.async;

import com.example.location.api.system.async.AsyncOpFailure;

public class DefaultAsyncOpFailure implements AsyncOpFailure {

    private String errorMessage;

    public DefaultAsyncOpFailure(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    @Override
    public String errorMessage() {
        return this.errorMessage;
    }
}
