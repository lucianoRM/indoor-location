package com.example.location.internal.entity.emitter;

import com.example.location.api.data.Position;
import com.example.location.api.data.Signal;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.entity.SkeletalIdentifiableObject;


public class SignalEmitterView extends SkeletalIdentifiableObject implements SignalEmitter {

    private Signal signal;
    private Position position;

    public SignalEmitterView(String id, String name, Signal signal, Position position) {
        super(id, name);
        this.signal = signal;
        this.position = position;
    }

    @Override
    public Signal getSignal() {
        return signal;
    }

    @Override
    public void emitSignal() {
        throw new UnsupportedOperationException("Not an active emitter");
    }

    @Override
    public Position getPosition() {
        return position;
    }
}
