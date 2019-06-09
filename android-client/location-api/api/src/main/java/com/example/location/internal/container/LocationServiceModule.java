package com.example.location.internal.container;

import com.example.location.internal.http.HttpLocationClient;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;

@Module
public class LocationServiceModule {

    private HttpLocationClient httpLocationClient;

    public LocationServiceModule(HttpLocationClient httpLocationClient) {
        this.httpLocationClient = httpLocationClient;
    }

    @Provides
    @Singleton
    public HttpLocationClient locationService() {
        return httpLocationClient;
    }
}
