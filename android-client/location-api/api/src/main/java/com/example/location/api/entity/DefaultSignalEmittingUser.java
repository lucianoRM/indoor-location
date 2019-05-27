package com.example.location.api.entity;

import com.example.location.api.data.Position;

public class DefaultSignalEmittingUser extends SkeletalUser implements SignalEmittingUser {

    public DefaultSignalEmittingUser(String id, String name, Position position) {
        super(id, name, position);
    }

}
