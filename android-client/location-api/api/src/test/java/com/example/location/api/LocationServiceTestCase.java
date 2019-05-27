package com.example.location.api;

import com.example.location.api.entity.User;
import com.example.location.api.http.LocationService;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import org.apache.commons.io.IOUtils;
import org.junit.Before;
import org.junit.Test;

import java.io.InputStream;

import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static java.nio.charset.StandardCharsets.UTF_8;

public class LocationServiceTestCase {
//    private static Gson gson = new GsonBuilder().registerTypeAdapter(User.class, new UserTypeAdapter()).create();

    private static final Retrofit retrofit = new Retrofit.Builder()
            .baseUrl("http://localhost:8082/")
            .addConverterFactory(GsonConverterFactory.create())
            .build();

    private LocationService locationService;
    private MockWebServer mockWebServer;

    @Before
    public void setUp() throws Exception{
        mockWebServer = new MockWebServer();
        mockWebServer.start(8082);

        locationService = retrofit.create(LocationService.class);
    }

    private String getJsonString(String name) throws Exception {
        InputStream user = this.getClass().getClassLoader().getResourceAsStream("sensing_user.json");
        return IOUtils.toString(user, UTF_8);

    }

    @Test
    public void createUser() throws Exception{
        mockWebServer.enqueue(new MockResponse().setBody(getJsonString("sensing_user.json")));

        Call<User> userCall = locationService.getUser("user");
        Response<User> response = userCall.execute();
    }

}
