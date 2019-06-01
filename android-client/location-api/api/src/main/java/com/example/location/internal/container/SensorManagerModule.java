package com.example.location.internal.container;

import com.example.location.internal.system.DefaultSensorManager;
import com.example.location.api.system.SensorManager;

import dagger.Binds;
import dagger.Module;

@Module
public abstract class SensorManagerModule {

    @Binds
    public abstract SensorManager sensorManager(DefaultSensorManager sensorManager);

}
