package com.example.location.internal.serialization;

import com.example.location.internal.entity.DefaultUser;
import com.example.location.internal.entity.User;

import java.lang.reflect.Type;

public class UserSerializer extends InterfaceSerializer<User> {

    @Override
    protected Type getImplementationTypeForDeserialization() {
        return DefaultUser.class;
    }
}
