package com.example.location.api.entity.sensor;

import com.example.location.api.data.Position;
import com.example.location.api.entity.SkeletalUser;


public class DefaultSensingUser extends SkeletalUser implements SensingUser {

    public DefaultSensingUser(String id, String name, Position position) {
        super(id, name, position);
    }

}
