package com.example.location.internal.container;

import com.example.location.internal.http.HttpLocationClient;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;
import retrofit2.Retrofit;

@Module
public class LocationServiceModule {

    @Provides
    @Singleton
    public HttpLocationClient locationService(Retrofit retrofit) {
       return retrofit.create(HttpLocationClient.class);
    }
}
