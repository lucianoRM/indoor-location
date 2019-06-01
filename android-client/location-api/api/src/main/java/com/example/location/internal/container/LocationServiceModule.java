package com.example.location.internal.container;

import com.example.location.internal.http.LocationService;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;

@Module
public class LocationServiceModule {

    private LocationService locationService;

    public LocationServiceModule(LocationService locationService) {
        this.locationService = locationService;
    }

    @Provides
    @Singleton
    public LocationService locationService() {
        return locationService;
    }
}
