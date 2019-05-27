package com.example.location.api.entity;

import com.example.location.api.data.Position;

public class DefaultSensingUser extends SkeletalUser implements SensingUser {

    public DefaultSensingUser(String id, String name, Position position) {
        super(id, name, position);
    }

}
