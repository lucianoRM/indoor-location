package com.example.location.internal.http;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.User;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Path;

public interface LocationService {

    String USERS_ENDPOINT = "/users";
    String SENSORS_ENDPOINT = "/sensors";
    String SIGNAL_EMITTERS_ENDPOINT = "/signal_emitters";

    @POST(USERS_ENDPOINT)
    void addUser(User user);

    @GET(SENSORS_ENDPOINT + "/{sensorId}")
    Call<Sensor> getSensor(@Path("sensorId") String sensorId);

    @GET(SIGNAL_EMITTERS_ENDPOINT + "/{signalEmitterId}")
    Call<SignalEmitter> getSignalEmitter(@Path("signalEmitterId") String signalEmitterId);

}
