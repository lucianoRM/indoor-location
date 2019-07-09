package com.example.location.internal.container;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.internal.serialization.SensorSerializer;
import com.example.location.internal.serialization.SignalEmitterSerializer;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;

@Module
public class GsonModule {

    @Provides
    @Singleton
    public Gson gson() {
        return new GsonBuilder()
                .registerTypeHierarchyAdapter(Sensor.class, new SensorSerializer())
                .registerTypeHierarchyAdapter(SignalEmitter.class, new SignalEmitterSerializer())
                .create();
    }

}
