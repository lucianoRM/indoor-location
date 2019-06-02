package com.example.location.integration;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.container.DaggerLocationSystemComponent;
import com.example.location.internal.container.LocationServiceModule;
import com.example.location.internal.container.LocationSystemComponent;
import com.example.location.internal.container.SensorManagerModule;
import com.example.location.internal.http.LocationService;
import com.example.location.internal.serialization.SignalEmitterSerializer;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class AbstractIntegrationTestCase {



}
