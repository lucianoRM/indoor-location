package com.example.location.internal.serialization;

import com.example.location.api.data.Signal;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.entity.emitter.DefaultSignalEmitter;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import org.junit.Test;

import static java.lang.String.format;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.MatcherAssert.assertThat;

public class SignalEmitterSerializerTestCase {

    private static Gson gson = new GsonBuilder()
            .registerTypeHierarchyAdapter(SignalEmitter.class, new SignalEmitterSerializer())
            .create();

    @Test
    public void serializeDeserialize() {
        Signal signal = new Signal();
        SignalEmitter signalEmitter = new DefaultSignalEmitter("id", "name", signal);
        SignalEmitter deserializedSignalEmitter = gson.fromJson(gson.toJson(signalEmitter), SignalEmitter.class);
        assertThat(deserializedSignalEmitter, is(equalTo(signalEmitter)));
    }

    @Test
    public void serializeDeserializeWithSignalAttributes() {
        Signal signal = new Signal();
        final String a1Key = "POWER";
        final String a1Value = Float.toString(100.0f);
        signal.addAttribute(a1Key, a1Value);
        SignalEmitter signalEmitter = new DefaultSignalEmitter("id", "name", signal);
        SignalEmitter deserializedSignalEmitter = gson.fromJson(gson.toJson(signalEmitter), SignalEmitter.class);
        assertThat(deserializedSignalEmitter, is(equalTo(signalEmitter)));
        Signal deserializedSignal = deserializedSignalEmitter.getSignal();
        assertThat(deserializedSignal.getAttribute(a1Key).get(), equalTo(a1Value));
    }

    @Test
    public void deserializeFromString() {
        final String id = "se";
        final String signalKey = "signalKey";
        final String signalValue = "signalValue";
        final float x = 110.4f;
        final float y = -23.3f;
        final String signalEmitterString = format("{\"id\":\"%s\", \"signal\" : {\"%s\":\"%s\"}, \"position\": {\"x\":%f, \"y\":%f}}", id, signalKey, signalValue,x,y);
        SignalEmitter signalEmitter = gson.fromJson(signalEmitterString, SignalEmitter.class);
        assertThat(signalEmitter.getId(), equalTo(id));
        assertThat(signalEmitter.getSignal().getAttribute(signalKey).get(), equalTo(signalValue));
        assertThat(signalEmitter.getPosition().getX(), equalTo(x));
        assertThat(signalEmitter.getPosition().getY(), equalTo(y));
    }
}
