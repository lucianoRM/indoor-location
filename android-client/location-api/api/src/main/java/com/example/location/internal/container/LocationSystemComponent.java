package com.example.location.internal.container;

import com.example.location.internal.http.HttpLocationClient;
import com.example.location.api.system.SensorManager;

import javax.inject.Singleton;

import dagger.Component;

@Singleton
@Component(modules = {
        LocationServiceModule.class,
        SensorManagerModule.class,
        EmitterManagerModule.class
})
public interface LocationSystemComponent {

    SensorManager sensorManager();
    HttpLocationClient locationService();

}
