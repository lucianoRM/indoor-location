package com.example.location.impl.emitter;

import com.example.location.api.data.Position;
import com.example.location.internal.entity.SkeletalUser;
import com.example.location.internal.entity.emitter.SignalEmittingUser;

public class NoOpSignalEmittingUser extends SkeletalUser implements SignalEmittingUser {

    public NoOpSignalEmittingUser(String id, String name, Position position) {
        super(id, name, position);
    }

    @Override
    public void emitSignal() {

    }
}
