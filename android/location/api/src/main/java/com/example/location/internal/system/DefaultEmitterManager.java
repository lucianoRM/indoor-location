package com.example.location.internal.system;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.system.EmitterAlreadyExistsException;
import com.example.location.api.system.EmitterManager;
import com.example.location.api.system.EmitterManagerException;
import com.example.location.internal.http.HttpCode;
import com.example.location.internal.http.HttpLocationClient;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import javax.inject.Inject;

import retrofit2.Call;
import retrofit2.Response;

import static com.example.location.internal.http.HttpCode.CONFLICT;
import static com.example.location.internal.http.HttpCode.codeFrom;
import static java.lang.System.nanoTime;
import static java.util.Collections.unmodifiableMap;
import static java.util.Optional.ofNullable;
import static java.util.concurrent.TimeUnit.NANOSECONDS;

public class DefaultEmitterManager implements EmitterManager {

    private static final int CACHE_VALUE_TTL_MINUTES = 1;
    private Long lastUpdatedTime;
    private Map<String, SignalEmitter> signalEmittersCache;
    private HttpLocationClient httpClient;

    @Inject
    public DefaultEmitterManager(HttpLocationClient httpClient) {
        this.httpClient = httpClient;
        this.signalEmittersCache = new HashMap<>();
    }

    @Override
    public void registerEmitter(SignalEmitter signalEmitter) throws EmitterManagerException {
        Call<SignalEmitter> httpCall = httpClient.registerSignalEmitter(signalEmitter);
        Response<SignalEmitter> httpResponse;
        try {
            httpResponse = httpCall.execute();
        }catch (IOException e) {
            throw new EmitterManagerException("Could not register signal emitter", e);
        }
        if(!httpResponse.isSuccessful()) {
            HttpCode responseCode = codeFrom(httpResponse.code());
            if(CONFLICT.equals(responseCode)) {
                throw new EmitterAlreadyExistsException("The emitter with id: " + signalEmitter.getId() + " already exists");
            }
        }
        lastUpdatedTime = null; //force cache to update on next call to see changes
    }

    @Override
    public Optional<SignalEmitter> getSignalEmitter(String id) throws EmitterManagerException{
        updateCacheIfNeeded();
        return ofNullable(signalEmittersCache.get(id));
    }

    @Override
    public Map<String,SignalEmitter> getSignalEmitters() throws EmitterManagerException {
        updateCacheIfNeeded();
        return unmodifiableMap(signalEmittersCache);
    }

    private boolean shouldUpdateCache() {
        //Check if data should be updated
        if (lastUpdatedTime == null || (NANOSECONDS.toMinutes(nanoTime() - lastUpdatedTime) > CACHE_VALUE_TTL_MINUTES)) {
            return true;
        }
        return false;
    }

    private void updateCacheIfNeeded() throws EmitterManagerException{
        if(!shouldUpdateCache()) {
            return;
        }
        Call<List<SignalEmitter>> httpCall = httpClient.getSignalEmitters();
        Response<List<SignalEmitter>> httpResponse;
        try {
            httpResponse = httpCall.execute();
        }catch (IOException e) {
            throw new EmitterManagerException("Error while getting signal emitters", e);
        }
        if(!httpResponse.isSuccessful()) {
            throw new EmitterManagerException(httpResponse.message());
        }
        signalEmittersCache = new HashMap<>();
        httpResponse.body().forEach(se -> signalEmittersCache.put(se.getId(), se));
        lastUpdatedTime = nanoTime();
    }
}
