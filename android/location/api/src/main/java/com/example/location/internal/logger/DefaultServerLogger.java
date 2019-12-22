package com.example.location.internal.logger;

import com.example.location.internal.http.HttpLocationClient;

import javax.inject.Inject;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class DefaultServerLogger implements ServerLogger {

    private static final Callback<String> NOOP_CALLBACK = new Callback<String>() {
        @Override
        public void onResponse(Call<String> call, Response<String> response) {}

        @Override
        public void onFailure(Call<String> call, Throwable t) {}
    };

    private HttpLocationClient client;

    @Inject
    public DefaultServerLogger(HttpLocationClient client) {
        this.client = client;
    }

    @Override
    public void logInServer(ServerLogEntry entry) {
        Call<String> call = client.logInServer(entry);
        call.enqueue(NOOP_CALLBACK);
    }
}
