package com.example.location.internal.http;

import com.example.location.api.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.User;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;

public interface HttpLocationClient {

    //TODO: Move endpoints to configuration
    String USERS_ENDPOINT = "/users";
    String SENSORS_ENDPOINT = "/sensors";
    String SIGNAL_EMITTERS_ENDPOINT = "/signal_emitters";

    /**
     * Get all {@link SignalEmitter}s registered in the server.
     * @return A {@link List<SignalEmitter>} containing all {@link SignalEmitter}s
     */
    @GET(SIGNAL_EMITTERS_ENDPOINT)
    Call<List<SignalEmitter>> getSignalEmitters();

    /**
     * Update last sensed objects for this sensor in the server.
     * @param sensorId the id of this sensor
     * @param sensedObjects all new objects being sensed
     * @return The sensor updated
     */
    @PUT(SENSORS_ENDPOINT + "/{sensorId}")
    Call<Sensor> udpateSensor(@Path("sensorId") String sensorId, @Body List<SensedObject> sensedObjects);

}
