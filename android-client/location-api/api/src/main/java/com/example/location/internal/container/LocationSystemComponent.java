package com.example.location.internal.container;

import com.example.location.api.system.EmitterManager;
import com.example.location.api.system.Locator;
import com.example.location.internal.config.SystemConfiguration;
import com.example.location.internal.http.HttpLocationClient;
import com.example.location.api.system.SensorManager;
import com.google.gson.Gson;

import javax.inject.Singleton;

import dagger.Component;
import okhttp3.OkHttpClient;

@Singleton
@Component(modules = {
        LocationServiceModule.class,
        SensorManagerModule.class,
        EmitterManagerModule.class,
        HttpClientModule.class,
        RetrofitModule.class,
        GsonModule.class,
        SystemConfigurationModule.class,
        LocatorModule.class
})
public interface LocationSystemComponent {

    SensorManager sensorManager();
    EmitterManager emitterManager();
    Gson gson();
    OkHttpClient httpClient();
    SystemConfiguration systemConfiguration();
    HttpLocationClient locationServiceClient();
    Locator locator();

}
