package com.example.location.internal.serialization;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.entity.emitter.DefaultSignalEmitter;

import java.lang.reflect.Type;

public class SignalEmitterSerializer extends TypedObjectSerializer<SignalEmitter> {

    @Override
    protected Type getImplementationTypeForDeserialization(String type) {
        return DefaultSignalEmitter.class;
    }

    @Override
    protected String getTypeForSerialization(SignalEmitter object) {
        //TODO: Fix this
        return "ANCHOR";
    }
}
