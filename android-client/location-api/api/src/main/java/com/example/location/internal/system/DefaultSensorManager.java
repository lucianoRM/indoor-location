package com.example.location.internal.system;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.system.EmitterManager;
import com.example.location.api.system.SensorAlreadyExistsException;
import com.example.location.api.system.SensorManager;
import com.example.location.api.system.SensorManagerException;
import com.example.location.internal.entity.sensor.DefaultSensor;
import com.example.location.internal.http.HttpCode;
import com.example.location.internal.http.HttpLocationClient;
import com.example.location.internal.http.HttpSensorListener;

import java.io.IOException;

import javax.inject.Inject;

import retrofit2.Call;
import retrofit2.Response;

import static com.example.location.internal.http.HttpCode.codeFrom;

public class DefaultSensorManager implements SensorManager {

    private HttpLocationClient httpLocationClient;
    private EmitterManager emitterManager;

    @Inject
    public DefaultSensorManager(HttpLocationClient httpLocationClient,
                                EmitterManager emitterManager) {
        this.httpLocationClient = httpLocationClient;
        this.emitterManager = emitterManager;
    }

    @Override
    public Sensor createSensor(SensorConfiguration config) throws SensorManagerException{
        final Sensor sensor =
                new DefaultSensor(
                        config.getSensorId(),
                        config.getSensorName(),
                        config.getSensorFeed(),
                        config.getDataTransformer(),
                        new HttpSensorListener(httpLocationClient),
                        emitterManager
                );

        Call<Sensor> httpCall = httpLocationClient.registerSensor(sensor);
        try {
            Response<Sensor> httpResponse = httpCall.execute();
            if(!httpResponse.isSuccessful()) {
                HttpCode responseCode = codeFrom(httpResponse.code());
                switch (responseCode) {
                    case CONFLICT:
                        throw new SensorAlreadyExistsException("The sensor with id: " + config.getSensorId() + " already exists");
                    case SERVER_ERROR:
                        throw new RuntimeException("Internal server error");
                    default:
                        break;
                }
            }
        }catch (IOException e) {
            throw new SensorManagerException("Could not connect to remote system",e);
        }
        return sensor;
    }
}
