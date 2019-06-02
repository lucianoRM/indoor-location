package com.example.location.internal.container;

import com.example.location.api.system.SensorManager;
import com.example.location.internal.system.DefaultSensorManager;


import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;

@Module
public class SensorManagerModule {

    @Provides
    @Singleton
    public SensorManager sensorManager(DefaultSensorManager sensorManagerImpl) {
        return sensorManagerImpl;
    }
}
