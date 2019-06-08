package com.example.location.functional;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.internal.container.DaggerLocationSystemComponent;
import com.example.location.internal.container.LocationServiceModule;
import com.example.location.internal.container.LocationSystemComponent;
import com.example.location.internal.container.SensorManagerModule;
import com.example.location.functional.http.HttpLocationClient;
import com.example.location.internal.serialization.SensorSerializer;
import com.example.location.internal.serialization.SignalEmitterSerializer;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import org.junit.Before;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.converter.scalars.ScalarsConverterFactory;

public abstract class AbstractFunctionalTestCase {

    private static final Gson GSON = new GsonBuilder()
            .registerTypeHierarchyAdapter(Sensor.class, new SensorSerializer())
            .registerTypeHierarchyAdapter(SignalEmitter.class, new SignalEmitterSerializer())
            .create();


    private Retrofit retrofit;
    private LocationSystemComponent container;

    @Before
    public void setUp() throws Exception{
        retrofit = new Retrofit.Builder()
                .baseUrl("http://localhost:" + getServerPort())
                .addConverterFactory(ScalarsConverterFactory.create())
                .addConverterFactory(GsonConverterFactory.create(GSON))
                .build();
        container = DaggerLocationSystemComponent
                .builder()
                .locationServiceModule(new LocationServiceModule(retrofit.create(HttpLocationClient.class)))
                .sensorManagerModule(new SensorManagerModule())
                .build();
    }


    protected LocationSystemComponent getContainer() {
        return this.container;
    }

    protected Gson getGson() {
        return GSON;
    }

    protected abstract int getServerPort();


}
