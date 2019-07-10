package com.example.location.internal.entity.emitter;

import com.example.location.api.data.Signal;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.entity.SkeletalIdentifiableObject;


public class SignalEmitterView extends SkeletalIdentifiableObject implements SignalEmitter {

    private Signal signal;

    public SignalEmitterView(String id, String name, Signal signal) {
        super(id, name);
        this.signal = signal;
    }

    @Override
    public Signal getSignal() {
        return signal;
    }

    @Override
    public void emitSignal() {
        throw new UnsupportedOperationException("Not an active emitter");
    }
}
