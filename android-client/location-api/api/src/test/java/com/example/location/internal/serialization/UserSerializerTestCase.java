package com.example.location.internal.serialization;

import com.example.location.api.data.Position;
import com.example.location.internal.entity.emitter.DefaultSignalEmittingUser;
import com.example.location.internal.entity.sensor.SensingUser;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.entity.emitter.SignalEmittingUser;
import com.example.location.api.entity.User;
import com.example.location.internal.entity.sensor.DefaultSensingUser;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.is;
import static org.junit.rules.ExpectedException.none;

public class UserSerializerTestCase {

    private static Gson gson = new GsonBuilder()
            .registerTypeHierarchyAdapter(User.class, new UserSerializer())
            .create();
    private static Position position = new Position(0, 0);

    @Rule
    public ExpectedException expectedException = none();

    @Test
    public void serializeDeserializeFromUserAsSensingUser() {
        User sensingUser = new DefaultSensingUser("user", "user", position);
        User deserializedUser = gson.fromJson(gson.toJson(sensingUser), User.class);
        assertThat(deserializedUser, is(equalTo(sensingUser)));
    }

    @Test
    public void serializeDeserializeFromUserAsSignalEmittingUser() {
        User signalEmittingUser = new DefaultSignalEmittingUser("user", "user", position);
        User deserializedUser = gson.fromJson(gson.toJson(signalEmittingUser), User.class);
        assertThat(deserializedUser, is(equalTo(signalEmittingUser)));
    }

    @Test
    public void serializeDeserializeFromSensor() {
        Sensor user = new DefaultSensingUser("user", "user", position);
        User deserializedUser = gson.fromJson(gson.toJson(user), User.class);
        assertThat(deserializedUser, is(equalTo((User)user)));
    }

    @Test
    public void serializeDeserializeFromSignalEmitter() {
        SignalEmitter user = new DefaultSignalEmittingUser("user", "user", position);
        User deserializedUser = gson.fromJson(gson.toJson(user), User.class);
        assertThat(deserializedUser, is(equalTo((User)user)));
    }

    @Test
    public void serializeDeserializeToSensor() {
        User user = new DefaultSensingUser("user", "user", position);
        User deserializedUser = gson.fromJson(gson.toJson(user), SensingUser.class);
        assertThat(deserializedUser, is(equalTo(user)));
    }

    @Test
    public void serializeDeserializeToSignalEmitter() {
        User user = new DefaultSignalEmittingUser("user", "user", position);
        User deserializedUser = gson.fromJson(gson.toJson(user), SignalEmittingUser.class);
        assertThat(deserializedUser, is(equalTo(user)));
    }

    @Test
    public void deserializeUserWithWrongType() {
        User user = new DefaultSignalEmittingUser("user", "user", position);
        JsonElement jsonElement = gson.toJsonTree(user);
        JsonObject jsonObject = jsonElement.getAsJsonObject();
        jsonObject.addProperty("type", "WRONG_TYPE");
        expectedException.expect(RuntimeException.class);
        gson.fromJson(jsonObject, User.class);
    }


}

