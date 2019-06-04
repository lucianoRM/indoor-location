package com.example.location.internal.system;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.system.EmitterManager;
import com.example.location.internal.http.HttpLocationClient;

import org.junit.Before;
import org.junit.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import retrofit2.Call;
import retrofit2.Response;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class DefaultEmitterManagerTestCase {

    private HttpLocationClient mockedHttpClient;
    private EmitterManager emitterManager;

    @Before
    public void setUp() {
        mockedHttpClient = mock(HttpLocationClient.class);
        emitterManager = new DefaultEmitterManager(mockedHttpClient);
    }

    @Test
    public void getsEmittersFromServer() throws Exception{
        final String emitterId = "id";
        SignalEmitter mockedEmitter = mock(SignalEmitter.class);
        when(mockedEmitter.getId()).thenReturn(emitterId);
        List<SignalEmitter> signalEmitters = new ArrayList<>();
        signalEmitters.add(mockedEmitter);
        Call<List<SignalEmitter>> mockedCall = mock(Call.class);
        Response<List<SignalEmitter>> mockedResponse = mock(Response.class);
        when(mockedResponse.body()).thenReturn(signalEmitters);
        when(mockedCall.execute()).thenReturn(mockedResponse);
        when(mockedHttpClient.getSignalEmitters()).thenReturn(mockedCall);

        Optional<SignalEmitter> emitter = emitterManager.getSignalEmitter(emitterId);
        assertThat(emitter, equalTo(mockedEmitter));
    }

}
