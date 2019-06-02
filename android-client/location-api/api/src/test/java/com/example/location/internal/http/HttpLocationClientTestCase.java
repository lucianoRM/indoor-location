package com.example.location.internal.http;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.serialization.SignalEmitterSerializer;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;


import org.apache.commons.io.IOUtils;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;

import java.io.InputStream;
import java.lang.reflect.Type;
import java.util.List;

import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static java.nio.charset.StandardCharsets.UTF_8;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.is;
import static org.junit.rules.ExpectedException.none;

public class HttpLocationClientTestCase {

    private static Gson gson = new GsonBuilder()
            .registerTypeHierarchyAdapter(SignalEmitter.class, new SignalEmitterSerializer())
            .create();

    private static final Retrofit retrofit = new Retrofit.Builder()
            .baseUrl("http://localhost:8082/")
            .addConverterFactory(GsonConverterFactory.create(gson))
            .build();

    private static Type signalEmitterListType = new TypeToken<List<SignalEmitter>>(){}.getType();

    private HttpLocationClient httpLocationClient;
    private MockWebServer mockWebServer;

    @Rule
    public ExpectedException expectedException = none();

    @Before
    public void setUp() throws Exception{
        mockWebServer = new MockWebServer();
        mockWebServer.start(8082);

        httpLocationClient = retrofit.create(HttpLocationClient.class);
    }

    @Test
    public void getSignalEmitters() throws Exception {
        String serializedSignalEmitters = getJsonString("signal_emitters.json");
        List<SignalEmitter> expectedSignalEmitters = gson.fromJson(serializedSignalEmitters, signalEmitterListType);
        mockWebServer.enqueue(new MockResponse().setBody(serializedSignalEmitters));
        Call<List<SignalEmitter>> signalEmittersCall = httpLocationClient.getSignalEmitters();
        Response<List<SignalEmitter>> response = signalEmittersCall.execute();
        List<SignalEmitter> receivedEmitters = response.body();
        assertThat(receivedEmitters, is(equalTo(expectedSignalEmitters)));
    }

    private String getJsonString(String name) throws Exception {
        InputStream user = this.getClass().getClassLoader().getResourceAsStream(name);
        return IOUtils.toString(user, UTF_8);

    }

}
