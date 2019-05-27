package com.example.location.api.serialization;

import com.example.location.api.entity.DefaultSensingUser;
import com.example.location.api.entity.DefaultSignalEmittingUser;
import com.example.location.api.entity.SensingUser;
import com.example.location.api.entity.SignalEmittingUser;
import com.example.location.api.entity.User;
import com.example.location.api.entity.UserType;
import com.google.gson.Gson;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonParseException;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;
import com.google.gson.TypeAdapter;
import com.google.gson.reflect.TypeToken;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonWriter;

import java.io.IOException;
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
