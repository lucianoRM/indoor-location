package com.example.location.internal.http;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.internal.data.SensedObject;
import com.example.location.internal.entity.sensor.SensorListener;
import com.example.location.internal.logger.ServerLogger;

import java.io.IOException;
import java.util.List;

import retrofit2.Call;
import retrofit2.Response;

import static com.example.location.internal.logger.ServerLogEntry.entry;
import static java.lang.String.format;
import static java.util.Arrays.asList;

/**
 * JUST FOR TESTING
 */
public class MeasurementsSensorListener implements SensorListener {

    private static final List<String> LOCATION_SERVICES = asList("optimized", "geometric", "simple");
    private HttpLocationClient httpLocationClient;
    private ServerLogger serverLogger;

    public MeasurementsSensorListener(HttpLocationClient httpLocationClient,
                                      ServerLogger serverLogger) {
        this.httpLocationClient = httpLocationClient;
        this.serverLogger = serverLogger;
    }

    private void executeAndLog(Sensor sensor, List<SensedObject> sensedObjects, String service) {
        Call<String> updateSensorCall = httpLocationClient.updateSensor(sensor.getId(), sensedObjects, service);
        try {
            Response<String> res = updateSensorCall.execute();
            if(!res.isSuccessful()) {
                throw new RuntimeException("Sensor update request unsuccessful " + res.errorBody().string());
            }
            serverLogger.logInServer(entry("SERVICE", format("Updating location from sensor: %s with service: %s", sensor.getId(), service)));
        }catch (IOException e) {
            //TODO: fix this
            throw new RuntimeException(e);
        }
    }

    @Override
    public void onSensorUpdate(Sensor sensor, List<SensedObject> sensedObjects) {
        for(String s: LOCATION_SERVICES) {
            executeAndLog(sensor, sensedObjects, s);
        }
    }
}
