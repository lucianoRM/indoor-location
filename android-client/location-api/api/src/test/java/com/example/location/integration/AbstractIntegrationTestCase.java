package com.example.location.integration;

import com.example.location.internal.container.DaggerLocationSystemComponent;
import com.example.location.internal.container.LocationServiceModule;
import com.example.location.internal.container.LocationSystemComponent;
import com.example.location.internal.http.LocationService;

import org.junit.Test;

import retrofit2.Retrofit;

public class AbstractIntegrationTestCase {

    private static final Retrofit retrofit = new Retrofit.Builder()
            .baseUrl("http://localhost:8082/")
            .build();

    private LocationSystemComponent container;

    public AbstractIntegrationTestCase() {
        this.container = DaggerLocationSystemComponent
                .builder()
                .locationServiceModule(new LocationServiceModule(retrofit.create(LocationService.class)))
                .build();
    }

    @Test
    public void test() {
        System.out.println(container.sensorManager());
        System.out.println(container.locationService());
    }
}
