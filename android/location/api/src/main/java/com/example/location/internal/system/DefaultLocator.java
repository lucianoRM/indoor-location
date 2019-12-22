package com.example.location.internal.system;

import com.example.location.api.data.Position;
import com.example.location.api.system.Locator;
import com.example.location.api.system.LocatorException;
import com.example.location.internal.entity.User;
import com.example.location.internal.http.HttpLocationClient;

import java.io.IOException;

import javax.inject.Inject;

import retrofit2.Call;
import retrofit2.Response;

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
    public Position getPosition() throws LocatorException {

        Call<User> userCall = httpLocationClient.getUser();
        try {
            Response<User> userResponse = userCall.execute();
            if (!userResponse.isSuccessful()) {
                throw new LocatorException(userResponse.message());
            } else {
                return userResponse.body().getPosition();
            }
        } catch (IOException e) {
            throw new LocatorException("Error getting user's position",e);
        }
    }
}
