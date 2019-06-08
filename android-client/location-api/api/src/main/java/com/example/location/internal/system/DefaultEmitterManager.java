package com.example.location.internal.system;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.system.EmitterManager;
import com.example.location.functional.http.HttpLocationClient;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import javax.inject.Inject;

import retrofit2.Call;
import retrofit2.Response;

import static java.util.Optional.ofNullable;

public class DefaultEmitterManager implements EmitterManager {

    private HttpLocationClient httpClient;
    private Map<String, SignalEmitter> signalEmitters = new HashMap<>();

    @Inject
    public DefaultEmitterManager(HttpLocationClient httpClient) {
        this.httpClient = httpClient;
    }

    @Override
    public Optional<SignalEmitter> getSignalEmitter(String id) {
        //TODO: Cache this
        Call<List<SignalEmitter>> httpCall = httpClient.getSignalEmitters();
        Response<List<SignalEmitter>> httpResponse;
        try {
            httpResponse = httpCall.execute();
        }catch (IOException e) {
            //TODO: Wrap exception
            throw new RuntimeException(e);
        }
        List<SignalEmitter> serverSignalEmitters = httpResponse.body();
        signalEmitters = new HashMap<>();
        serverSignalEmitters.forEach(se -> signalEmitters.put(se.getId(), se));
        return ofNullable(signalEmitters.get(id));
    }
}
