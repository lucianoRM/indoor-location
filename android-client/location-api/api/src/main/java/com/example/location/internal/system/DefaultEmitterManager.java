package com.example.location.internal.system;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.system.EmitterAlreadyExistsException;
import com.example.location.api.system.EmitterManager;
import com.example.location.api.system.EmitterManagerException;
import com.example.location.internal.http.HttpCode;
import com.example.location.internal.http.HttpLocationClient;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import javax.inject.Inject;

import retrofit2.Call;
import retrofit2.Response;

import static com.example.location.internal.http.HttpCode.CONFLICT;
import static com.example.location.internal.http.HttpCode.codeFrom;
import static java.util.Optional.ofNullable;

public class DefaultEmitterManager implements EmitterManager {

    private HttpLocationClient httpClient;
    private Map<String, SignalEmitter> signalEmitters = new HashMap<>();

    @Inject
    public DefaultEmitterManager(HttpLocationClient httpClient) {
        this.httpClient = httpClient;
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
    }

    @Override
    public Optional<SignalEmitter> getSignalEmitter(String id) throws EmitterManagerException{
        //TODO: Cache this
        Call<List<SignalEmitter>> httpCall = httpClient.getSignalEmitters();
        Response<List<SignalEmitter>> httpResponse;
        try {
            httpResponse = httpCall.execute();
        }catch (IOException e) {
            throw new EmitterManagerException("Error while getting signal emitters", e);
        }
        List<SignalEmitter> serverSignalEmitters = httpResponse.body();
        signalEmitters = new HashMap<>();
        serverSignalEmitters.forEach(se -> signalEmitters.put(se.getId(), se));
        return ofNullable(signalEmitters.get(id));
    }
}
