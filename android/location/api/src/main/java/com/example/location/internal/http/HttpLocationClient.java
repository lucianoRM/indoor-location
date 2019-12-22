package com.example.location.internal.http;

import com.example.location.internal.entity.User;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.internal.data.SensedObject;
import com.example.location.internal.logger.ServerLogEntry;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;
import retrofit2.http.Query;

public interface HttpLocationClient {

    String USER_ID_PLACEHOLDER = "$USER_ID$";

    //TODO: Move endpoints to configuration
    String USERS_ENDPOINT = "/users";

    String ANCHORS_ENDPOINT = "/anchors";

    String SENSOR_ID_URL_PARAM = "sensorId";
    String SENSOR_ID_PLACEHOLDER = "/{" + SENSOR_ID_URL_PARAM + "}";
    String MY_SENSORS_ENDPOINT = USERS_ENDPOINT + "/" + USER_ID_PLACEHOLDER + "/sensors";

    String SIGNAL_EMITTERS_ENDPOINT = "/signal_emitters";
    String SIGNAL_EMITTER_URL_PARAM = "signalEmitterId";
    String SIGNAL_EMITTER_ID_PLACEHOLDER = "/{" + SIGNAL_EMITTER_URL_PARAM + "}";
    String MY_SIGNAL_EMITTERS_ENDPOINT = USERS_ENDPOINT + "/" + USER_ID_PLACEHOLDER + SIGNAL_EMITTERS_ENDPOINT;

    String LOG_ENDPOINT = "/log";

    /**
     * Register a new {@link SignalEmitter}
     * @param signalEmitter the {@link SignalEmitter} to be registered
     * @return the signal emitter registered
     */
    @POST(MY_SIGNAL_EMITTERS_ENDPOINT)
    Call<SignalEmitter> registerSignalEmitter(@Body SignalEmitter signalEmitter);

    /**
     * Get the {@link SignalEmitter} registered with the provided id.
     * @return A {@link SignalEmitter}
     */
    @GET(SIGNAL_EMITTERS_ENDPOINT + SIGNAL_EMITTER_ID_PLACEHOLDER)
    Call<SignalEmitter> getSignalEmitter(@Path(SIGNAL_EMITTER_URL_PARAM) String signalEmitterId);

    /**
     * Get all {@link SignalEmitter}s registered in the server.
     * @return A {@link List<SignalEmitter>} containing all {@link SignalEmitter}s
     */
    @GET(SIGNAL_EMITTERS_ENDPOINT)
    Call<List<SignalEmitter>> getSignalEmitters();

    /**
     * Get the {@link Sensor} from the server.
     * @param sensorId the id of the sensor to get
     * @return the sensor in the server
     */
    @GET(MY_SENSORS_ENDPOINT + SENSOR_ID_PLACEHOLDER)
    Call<Sensor> getSensor(@Path(SENSOR_ID_URL_PARAM) String sensorId);

    /**
     * Register a new {@link Sensor} in the server
     * @param sensor the sensor to be registered in the server
     * @return the sensor being registered
     */
    @POST(MY_SENSORS_ENDPOINT)
    Call<Sensor> registerSensor(@Body Sensor sensor);

    /**
     * Update last sensed objects for this sensor in the server.
     * @param sensorId the id of this sensor
     * @param sensedObjects all new objects being sensed
     * @param locationService the name of the location service to use
     */
    @PUT(MY_SENSORS_ENDPOINT + SENSOR_ID_PLACEHOLDER)
    Call<String> updateSensor(@Path(SENSOR_ID_URL_PARAM) String sensorId,
                              @Body List<SensedObject> sensedObjects,
                              @Query("location_service") String locationService);

    /**
     * Get the User(ME) from the server
     */
    @GET(USERS_ENDPOINT + "/" + USER_ID_PLACEHOLDER)
    Call<User> getUser();

    /**
     * Log to server
     */
    @POST(LOG_ENDPOINT)
    Call<String> logInServer(@Body ServerLogEntry logMessage);
}
