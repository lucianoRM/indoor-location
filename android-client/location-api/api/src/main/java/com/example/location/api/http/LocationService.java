package com.example.location.api.http;

import com.example.location.api.entity.User;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Path;

public interface LocationService {

    @POST("/users")
    void addUser(User user);

    @GET("/users/{userId}")
    Call<User> getUser(@Path("userId") String userId);

}
