package com.example.location.integration;

import com.example.location.internal.entity.User;

import org.junit.Test;

import retrofit2.Call;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;

public class UserIntegrationTestCase extends AbstractIntegrationTestCase {

    @Test
    public void getUser() throws Exception {
        Call<User> getUserCall = locationClient().getUser();
        User user = getUserCall.execute().body();
        assertThat(user.getId(), equalTo(USER_ID));
    }

}
