package com.example.location.functional;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.internal.container.DaggerLocationSystemComponent;
import com.example.location.internal.container.LocationServiceModule;
import com.example.location.internal.container.LocationSystemComponent;
import com.example.location.internal.container.SensorManagerModule;
import com.example.location.internal.http.HttpLocationClient;
import com.example.location.internal.serialization.SensorSerializer;
import com.example.location.internal.serialization.SignalEmitterSerializer;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import net.bytebuddy.build.ToStringPlugin;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.util.List;

import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.converter.scalars.ScalarsConverterFactory;
import retrofit2.http.POST;

public class AbstractFunctionalTestCase {

    private static final int PORT = 8085;

    private static final Gson GSON = new GsonBuilder()
            .registerTypeHierarchyAdapter(Sensor.class, new SensorSerializer())
            .registerTypeHierarchyAdapter(SignalEmitter.class, new SignalEmitterSerializer())
            .create();

    private static final Retrofit RETROFIT = new Retrofit.Builder()
            .baseUrl("http://localhost:" + PORT)
            .addConverterFactory(ScalarsConverterFactory.create())
            .addConverterFactory(GsonConverterFactory.create(GSON))
            .build();

    private MockWebServer mockWebServer;
    private LocationSystemComponent container;

    @Before
    public void setUp() throws Exception{
        mockWebServer = new MockWebServer();
        mockWebServer.start(PORT);
        container = DaggerLocationSystemComponent
                .builder()
                .locationServiceModule(new LocationServiceModule(RETROFIT.create(HttpLocationClient.class)))
                .sensorManagerModule(new SensorManagerModule())
                .build();
    }

    @After
    public void tearDown() throws Exception{
        mockWebServer.shutdown();
    }

    protected MockWebServer getMockedServer() {
        return mockWebServer;
    }

    protected LocationSystemComponent getContainer() {
        return this.container;
    }

    protected Gson getGson() {
        return GSON;
    }
}
