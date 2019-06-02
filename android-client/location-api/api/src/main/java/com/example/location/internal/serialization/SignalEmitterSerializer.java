package com.example.location.internal.serialization;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.entity.emitter.DefaultSignalEmitter;

import java.lang.reflect.Type;

public class SignalEmitterSerializer extends TypedObjectSerializer<SignalEmitter> {

    @Override
    protected Type getImplementationTypeFor(String type) {
        return DefaultSignalEmitter.class;
    }

    @Override
    protected String getTypeFor(SignalEmitter object) {
        //TODO: Fix this
        return "ANCHOR";
    }
}
