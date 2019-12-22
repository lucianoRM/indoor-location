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

import static java.util.Collections.singletonList;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static retrofit2.Response.success;

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
        Call<List<SignalEmitter>> mockedCall = mock(Call.class);
        Response<List<SignalEmitter>> response = success(singletonList(mockedEmitter));
        when(mockedCall.execute()).thenReturn(response);
        when(mockedHttpClient.getSignalEmitters()).thenReturn(mockedCall);

        Optional<SignalEmitter> emitter = emitterManager.getSignalEmitter(emitterId);
        assertThat(emitter.get(), equalTo(mockedEmitter));
    }

    @Test
    public void signalEmittersAreCached() throws Exception {
        final String emitterId1 = "id1";
        SignalEmitter mockedEmitter1 = mock(SignalEmitter.class);
        when(mockedEmitter1.getId()).thenReturn(emitterId1);
        final String emitterId2 = "id2";
        SignalEmitter mockedEmitter2 = mock(SignalEmitter.class);
        when(mockedEmitter2.getId()).thenReturn(emitterId2);

        List<SignalEmitter> signalEmitterList = new ArrayList<>();
        signalEmitterList.add(mockedEmitter1);
        signalEmitterList.add(mockedEmitter2);

        Call<List<SignalEmitter>> mockedCall = mock(Call.class);
        Response<List<SignalEmitter>> response = success(signalEmitterList);
        when(mockedCall.execute()).thenReturn(response);
        when(mockedHttpClient.getSignalEmitters()).thenReturn(mockedCall);

        assertThat(emitterManager.getSignalEmitter(emitterId1).get(), equalTo(mockedEmitter1));
        assertThat(emitterManager.getSignalEmitter(emitterId2).get(), equalTo(mockedEmitter2));

        assertThat(emitterManager.getSignalEmitter("not existent").isPresent(), equalTo(false));
        verify(mockedCall, times(1)).execute();
    }

    @Test
    public void cacheIsUpdatedIfEmitterIsAdded() throws Exception{
        final String emitterId1 = "id1";
        SignalEmitter mockedEmitter1 = mock(SignalEmitter.class);
        when(mockedEmitter1.getId()).thenReturn(emitterId1);

        Call<List<SignalEmitter>> mockedCall = mock(Call.class);
        Response<List<SignalEmitter>> response = success(singletonList(mockedEmitter1));
        when(mockedCall.execute()).thenReturn(response);
        when(mockedHttpClient.getSignalEmitters()).thenReturn(mockedCall);

        assertThat(emitterManager.getSignalEmitter(emitterId1).get(), equalTo(mockedEmitter1));
        assertThat(emitterManager.getSignalEmitter(emitterId1).get(), equalTo(mockedEmitter1));
        assertThat(emitterManager.getSignalEmitter(emitterId1).get(), equalTo(mockedEmitter1));
        verify(mockedCall, times(1)).execute();

        Call<SignalEmitter> registerEmitterCall = mock(Call.class);
        when(registerEmitterCall.execute()).thenReturn(success(null));
        when(mockedHttpClient.registerSignalEmitter(any())).thenReturn(registerEmitterCall);

        emitterManager.registerEmitter(mockedEmitter1);
        assertThat(emitterManager.getSignalEmitter(emitterId1).get(), equalTo(mockedEmitter1));
        assertThat(emitterManager.getSignalEmitter(emitterId1).get(), equalTo(mockedEmitter1));
        assertThat(emitterManager.getSignalEmitter(emitterId1).get(), equalTo(mockedEmitter1));
        verify(mockedCall, times(2)).execute(); //one before, one now

    }

}
