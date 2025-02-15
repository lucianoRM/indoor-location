package com.example.location.functional.http;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.functional.MockedServerFunctionalTestCase;
import com.example.location.internal.http.HttpLocationClient;
import com.google.gson.reflect.TypeToken;


import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;

import java.lang.reflect.Type;
import java.util.List;

import okhttp3.mockwebserver.MockResponse;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static com.example.location.TestUtils.readFile;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.is;
import static org.junit.rules.ExpectedException.none;

public class HttpLocationClientTestCase extends MockedServerFunctionalTestCase {

    private static Type signalEmitterListType = new TypeToken<List<SignalEmitter>>(){}.getType();

    @Rule
    public ExpectedException expectedException = none();

    @Test
    public void getSignalEmitters() throws Exception {
        String serializedSignalEmitters = readFile("signal_emitters.json");
        List<SignalEmitter> expectedSignalEmitters = getGson().fromJson(serializedSignalEmitters, signalEmitterListType);
        getMockedServer().enqueue(new MockResponse().setBody(serializedSignalEmitters));
        Call<List<SignalEmitter>> signalEmittersCall = locationClient().getSignalEmitters();
        Response<List<SignalEmitter>> response = signalEmittersCall.execute();
        List<SignalEmitter> receivedEmitters = response.body();
        assertThat(receivedEmitters, is(equalTo(expectedSignalEmitters)));
    }

    @Test
    public void getSignalEmitterById() throws Exception {
        final String id = "seId";
        String serializedSignalEmitter = readFile("signal_emitter.json");
        SignalEmitter expectedSignalEmitter = getGson().fromJson(serializedSignalEmitter, SignalEmitter.class);
        getMockedServer().enqueue(new MockResponse().setBody(serializedSignalEmitter));
        Call<SignalEmitter> signalEmittersCall = locationClient().getSignalEmitter(id);
        Response<SignalEmitter> response = signalEmittersCall.execute();
        SignalEmitter receivedEmitter = response.body();
        assertThat(receivedEmitter, is(equalTo(expectedSignalEmitter)));
    }



}
