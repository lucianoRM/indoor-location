package com.example.location.internal.http;

import com.example.location.api.entity.User;
import com.example.location.internal.serialization.UserSerializer;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;


import org.apache.commons.io.IOUtils;
import org.junit.Before;
import org.junit.Rule;
import org.junit.rules.ExpectedException;

import java.io.InputStream;

import okhttp3.mockwebserver.MockWebServer;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static com.example.location.UserMatcher.user;
import static java.nio.charset.StandardCharsets.UTF_8;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.is;
import static org.junit.rules.ExpectedException.none;

public class LocationServiceTestCase {

    private static Gson gson = new GsonBuilder()
            .registerTypeHierarchyAdapter(User.class, new UserSerializer())
            .create();

    private static final Retrofit retrofit = new Retrofit.Builder()
            .baseUrl("http://localhost:8082/")
            .addConverterFactory(GsonConverterFactory.create(gson))
            .build();

    private LocationService locationService;
    private MockWebServer mockWebServer;

    @Rule
    public ExpectedException expectedException = none();

    @Before
    public void setUp() throws Exception{
        mockWebServer = new MockWebServer();
        mockWebServer.start(8082);

        locationService = retrofit.create(LocationService.class);
    }

//    @Test
//    public void getSensingUser() throws Exception{
//        String serializedUser = getJsonString("sensing_user.json");
//        User expectedUser = gson.fromJson(serializedUser, User.class);
//        mockWebServer.enqueue(new MockResponse().setBody(serializedUser));
//        Call<User> userCall = locationService.getUser("user");
//        Response<User> response = userCall.execute();
//        User receivedUser = response.body();
//        assertThat(receivedUser, is(user(expectedUser)));
//    }
//
//    @Test
//    public void getSignalEmittingUser() throws Exception {
//        String serializedUser = getJsonString("signal_emitting_user.json");
//        User expectedUser = gson.fromJson(serializedUser, User.class);
//        mockWebServer.enqueue(new MockResponse().setBody(serializedUser));
//        Call<User> userCall = locationService.getUser("user");
//        Response<User> response = userCall.execute();
//        User receivedUser = response.body();
//        assertThat(receivedUser, is(user(expectedUser)));
//    }
//
//    @Test
//    public void getUnknownTypeUser() throws Exception{
//        String serializedUser = getJsonString("unknown_type_user.json");
//        mockWebServer.enqueue(new MockResponse().setBody(serializedUser));
//        Call<User> userCall = locationService.getUser("user");
//        expectedException.expectMessage("is not a valid user type");
//        userCall.execute();
//    }

    private String getJsonString(String name) throws Exception {
        InputStream user = this.getClass().getClassLoader().getResourceAsStream(name);
        return IOUtils.toString(user, UTF_8);

    }

}
