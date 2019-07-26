package com.example.location.internal.system;

import com.example.location.api.data.Position;
import com.example.location.api.system.Locator;
import com.example.location.internal.entity.User;
import com.example.location.internal.http.HttpLocationClient;

import java.io.IOException;

import javax.inject.Inject;

import retrofit2.Call;

/**
 * {@link Locator} implementation that finds the user by calling the http server and getting it's position.
 */
public class DefaultLocator implements Locator {

    private HttpLocationClient httpLocationClient;

    @Inject
    public DefaultLocator(HttpLocationClient httpLocationClient) {
        this.httpLocationClient = httpLocationClient;
    }

    @Override
    public Position getPosition() {
        Call<User> userCall = httpLocationClient.getUser();
        User user;
        try {
            user = userCall.execute().body();
        }catch (IOException e) {
            //TODO: FIX THIS
            throw new RuntimeException(e);
        }
        return user.getPosition();
    }
}
