package com.example.location.internal.system;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.system.EmitterManager;
import com.example.location.api.system.SensorAlreadyExistsException;
import com.example.location.api.system.SensorManager;
import com.example.location.api.system.SensorManagerException;
import com.example.location.internal.entity.sensor.DefaultSensor;
import com.example.location.internal.entity.sensor.SensorListener;
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
    private SensorListener sensorListener;

    @Inject
    public DefaultSensorManager(HttpLocationClient httpLocationClient,
                                EmitterManager emitterManager) {
        this.httpLocationClient = httpLocationClient;
        this.emitterManager = emitterManager;
        this.sensorListener = new HttpSensorListener(httpLocationClient);
    }

    @Override
    public Sensor getOrCreateSensor(SensorConfiguration config) throws SensorManagerException {
        Sensor sensor = createSensorLocally(config);
        if(!isSensorAlreadyRegistered(config.getSensorId())) {
           registerSensorInServer(sensor);
        }
        return sensor;
    }

    @Override
    public Sensor createSensor(SensorConfiguration config) throws SensorManagerException {
        Sensor sensor = createSensorLocally(config);
        registerSensorInServer(sensor);
        return sensor;
    }

    private boolean isSensorAlreadyRegistered(String sensorId) throws SensorManagerException {
        Call<Sensor> httpCall = httpLocationClient.getSensor(sensorId);
        try {
            Response<Sensor> httpResponse = httpCall.execute();
            if (!httpResponse.isSuccessful()) {
                HttpCode responseCode = codeFrom(httpResponse.code());
                switch (responseCode) {
                    case NOT_FOUND:
                        return false;
                    case SERVER_ERROR:
                        throw new SensorManagerException("Internal server error");
                    default:
                        break;
                }
            }
        } catch (IOException e) {
            throw new SensorManagerException("Could not connect to remote system", e);
        }
        return true;
    }

    private Sensor createSensorLocally(SensorConfiguration config) {
        return new DefaultSensor(
                config.getSensorId(),
                config.getSensorName(),
                config.getSensorFeed(),
                config.getDataTransformer(),
                sensorListener,
                emitterManager
        );
    }

    private void registerSensorInServer(Sensor sensor) throws SensorManagerException {
        Call<Sensor> httpCall = httpLocationClient.registerSensor(sensor);
        try {
            Response<Sensor> httpResponse = httpCall.execute();
            if (!httpResponse.isSuccessful()) {
                HttpCode responseCode = codeFrom(httpResponse.code());
                switch (responseCode) {
                    case CONFLICT:
                        throw new SensorAlreadyExistsException("The sensor with id: " + sensor.getId() + " already exists");
                    case SERVER_ERROR:
                        throw new SensorManagerException("Internal server error");
                    default:
                        break;
                }
            }
        } catch (IOException e) {
            throw new SensorManagerException("Could not connect to remote system", e);
        }
    }
}
