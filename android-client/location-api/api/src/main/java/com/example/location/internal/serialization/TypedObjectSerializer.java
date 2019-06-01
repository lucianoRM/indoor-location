package com.example.location.internal.serialization;

import com.google.gson.Gson;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;

import java.lang.reflect.Type;

public abstract class TypedObjectSerializer<T> implements JsonSerializer<T>, JsonDeserializer<T> {

    //This GSON is an instance with no typeAdapter registered.
    private static final Gson DEFAULT_GSON = new Gson();

    private static final String TYPE_KEY = "type";

    @Override
    public JsonElement serialize(T src, Type typeOfSrc, JsonSerializationContext context) {
        JsonElement serializedElement = DEFAULT_GSON.toJsonTree(src);
        JsonObject serializedObject = serializedElement.getAsJsonObject();
        serializedObject.addProperty(TYPE_KEY, getTypeFor(src));
        return serializedObject;
    }

    @Override
    public T deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context) throws JsonParseException {
        JsonObject jsonObject = json.getAsJsonObject();
        String type = jsonObject.get(TYPE_KEY).getAsString();
        return DEFAULT_GSON.fromJson(jsonObject, getImplementationTypeFor(type));
    }

    protected abstract Type getImplementationTypeFor(String type);

    protected abstract String getTypeFor(T object);

}
