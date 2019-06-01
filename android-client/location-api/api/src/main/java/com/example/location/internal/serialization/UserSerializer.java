package com.example.location.internal.serialization;

import com.example.location.internal.entity.emitter.DefaultSignalEmittingUser;
import com.example.location.api.entity.sensor.SensingUser;
import com.example.location.api.entity.emitter.SignalEmittingUser;
import com.example.location.api.entity.User;
import com.example.location.api.entity.UserType;
import com.example.location.internal.entity.sensor.DefaultSensingUser;

import java.lang.reflect.Type;

import static com.example.location.api.entity.UserType.ANCHOR;
import static com.example.location.api.entity.UserType.SENSOR;
import static com.example.location.api.entity.UserType.valueOf;

public class UserSerializer extends TypedObjectSerializer<User> {

    @Override
    protected Type getImplementationTypeFor(String type) {
        try {
            UserType userType = valueOf(type);
            if(SENSOR.equals(userType)) {
                return DefaultSensingUser.class;
            }
            if(ANCHOR.equals(userType)) {
                return DefaultSignalEmittingUser.class;
            }
        }catch (IllegalArgumentException e) {
            //exception below will be thrown
        }
        throw new RuntimeException(type + " is not a valid user type");
    }

    @Override
    protected String getTypeFor(User object) {
        if(object instanceof SensingUser) {
            return SENSOR.toString();
        }
        if(object instanceof SignalEmittingUser) {
            return ANCHOR.toString();
        }
        throw new RuntimeException("Unexpected user type: " + object);
    }
}
