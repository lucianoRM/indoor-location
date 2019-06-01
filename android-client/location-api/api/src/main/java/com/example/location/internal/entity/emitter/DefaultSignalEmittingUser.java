package com.example.location.internal.entity.emitter;

import com.example.location.api.data.Position;
import com.example.location.internal.entity.SkeletalUser;
import com.example.location.api.entity.emitter.SignalEmittingUser;

public class DefaultSignalEmittingUser extends SkeletalUser implements SignalEmittingUser {

    public DefaultSignalEmittingUser(String id, String name, Position position) {
        super(id, name, position);
    }

    @Override
    public void emitSignal() {

    }
}
