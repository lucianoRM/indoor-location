package com.example.location.internal.entity.emitter;

import com.example.location.api.data.Position;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.entity.SkeletalIdentifiableObject;

public class DefaultSignalEmitter extends SkeletalIdentifiableObject implements SignalEmitter {

    public DefaultSignalEmitter(String id, String name, Position position) {
        super(id, name, position);
    }

    @Override
    public void emitSignal() {

    }
}
