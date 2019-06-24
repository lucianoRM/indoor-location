package com.example.location.api.system;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.internal.container.DaggerLocationSystemComponent;
import com.example.location.internal.container.EmitterManagerModule;
import com.example.location.internal.container.LocationServiceModule;
import com.example.location.internal.container.LocationSystemComponent;
import com.example.location.internal.container.SensorManagerModule;
import com.example.location.internal.http.HttpLocationClient;
import com.example.location.internal.serialization.SensorSerializer;
import com.example.location.internal.serialization.SignalEmitterSerializer;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.converter.scalars.ScalarsConverterFactory;

public final class LocationSystem {

    private static final Gson GSON = new GsonBuilder()
            .registerTypeHierarchyAdapter(Sensor.class, new SensorSerializer())
            .registerTypeHierarchyAdapter(SignalEmitter.class, new SignalEmitterSerializer())
            .create();

    private LocationSystemComponent locationSystemComponent;

    public LocationSystem() {


        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://192.168.1.6:8082")
                .addConverterFactory(ScalarsConverterFactory.create())
                .addConverterFactory(GsonConverterFactory.create(GSON))
                .build();
        this.locationSystemComponent = DaggerLocationSystemComponent
                .builder()
                .locationServiceModule(new LocationServiceModule(retrofit.create(HttpLocationClient.class)))
                .sensorManagerModule(new SensorManagerModule())
                .emitterManagerModule(new EmitterManagerModule())
                .build();
    }

    public LocationSystemComponent getContainer() {
        return locationSystemComponent;
    }

}
