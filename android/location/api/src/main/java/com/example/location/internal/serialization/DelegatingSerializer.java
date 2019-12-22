package com.example.location.internal.serialization;

import com.google.gson.Gson;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonSerializer;

public abstract class DelegatingSerializer<T> implements JsonSerializer<T>, JsonDeserializer<T> {

    private static final Gson GSON = new Gson();

    protected Gson getGson() {
        return GSON;
    }

}
