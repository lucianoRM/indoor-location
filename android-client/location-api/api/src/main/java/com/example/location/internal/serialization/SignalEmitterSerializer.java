package com.example.location.internal.serialization;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.entity.emitter.SignalEmitterView;

import java.lang.reflect.Type;

public class SignalEmitterSerializer extends InterfaceSerializer<SignalEmitter> {

    @Override
    protected Type getImplementationTypeForDeserialization() {
        return SignalEmitterView.class;
    }

}
