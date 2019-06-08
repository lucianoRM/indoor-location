package com.example.location.internal.http;

import com.example.location.internal.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.emitter.SignalEmitter;

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
     * Register a new {@link Sensor} in the server
     * @param sensor the sensor to be registered in the server
     * @return the sensor being registered
     */
    @POST(SENSORS_ENDPOINT)
    Call<Sensor> registerSensor(@Body Sensor sensor);

    /**
     * Update last sensed objects for this sensor in the server.
     * @param sensorId the id of this sensor
     * @param sensedObjects all new objects being sensed
     */
    @PUT(SENSORS_ENDPOINT + "/{sensorId}")
    Call<String> updateSensor(@Path("sensorId") String sensorId, @Body List<SensedObject> sensedObjects);

}
