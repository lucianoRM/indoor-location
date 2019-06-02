package com.example.location.functional;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.container.DaggerLocationSystemComponent;
import com.example.location.internal.container.LocationServiceModule;
import com.example.location.internal.container.LocationSystemComponent;
import com.example.location.internal.container.SensorManagerModule;
import com.example.location.internal.http.HttpLocationClient;
import com.example.location.internal.serialization.SignalEmitterSerializer;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import org.junit.Before;

import okhttp3.mockwebserver.MockWebServer;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class AbstractFunctionalTestCase {

    private static final int PORT = 8085;

    private static final Gson GSON = new GsonBuilder()
            .registerTypeHierarchyAdapter(SignalEmitter.class, new SignalEmitterSerializer())
            .create();

    private static final Retrofit RETROFIT = new Retrofit.Builder()
            .baseUrl("http://localhost:" + PORT + "/")
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

    protected MockWebServer getMockedServer() {
        return mockWebServer;
    }

    protected LocationSystemComponent getContainer() {
        return this.container;
    }
}
