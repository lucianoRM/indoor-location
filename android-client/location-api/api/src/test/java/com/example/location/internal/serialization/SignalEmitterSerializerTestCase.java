package com.example.location.internal.serialization;

import com.example.location.api.data.Position;
import com.example.location.api.data.Signal;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.entity.emitter.DefaultSignalEmitter;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import org.junit.Test;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.MatcherAssert.assertThat;

public class SignalEmitterSerializerTestCase {

    private static Gson gson = new GsonBuilder()
            .registerTypeHierarchyAdapter(SignalEmitter.class, new SignalEmitterSerializer())
            .create();

    private static Position position = new Position(0, 0);

    @Test
    public void serializeDeserialize() {
        Signal signal = new Signal();
        SignalEmitter signalEmitter = new DefaultSignalEmitter("id", "name", position, signal);
        SignalEmitter deserializedSignalEmitter = gson.fromJson(gson.toJson(signalEmitter), SignalEmitter.class);
        assertThat(deserializedSignalEmitter, is(equalTo(signalEmitter)));
    }

    @Test
    public void serializeDeserializeWithSignalAttributes() {
        Signal signal = new Signal();
        final String a1Key = "POWER";
        final String a1Value = Float.toString(100.0f);
        signal.addAttribute(a1Key, a1Value);
        SignalEmitter signalEmitter = new DefaultSignalEmitter("id", "name", position, signal);
        SignalEmitter deserializedSignalEmitter = gson.fromJson(gson.toJson(signalEmitter), SignalEmitter.class);
        assertThat(deserializedSignalEmitter, is(equalTo(signalEmitter)));
        Signal deserializedSignal = deserializedSignalEmitter.getSignal();
        assertThat(deserializedSignal.getAttribute(a1Key).get(), equalTo(a1Value));
    }

}
