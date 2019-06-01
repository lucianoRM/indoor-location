package com.example.location.internal.container;

import com.example.location.internal.http.LocationService;
import com.example.location.api.system.SensorManager;

import javax.inject.Singleton;

import dagger.Component;

@Singleton
@Component(modules = {
        LocationServiceModule.class,
        SensorManagerModule.class
})
public interface LocationSystemComponent {

    SensorManager sensorManager();
    LocationService locationService();

}
