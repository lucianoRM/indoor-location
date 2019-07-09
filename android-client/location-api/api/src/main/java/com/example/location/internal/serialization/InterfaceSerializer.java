package com.example.location.internal.serialization;

import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import com.google.gson.JsonSerializationContext;

import java.lang.reflect.Type;

public abstract class InterfaceSerializer<T> extends DelegatingSerializer<T> {

    @Override
    public JsonElement serialize(T src, Type typeOfSrc, JsonSerializationContext context) {
        JsonElement serializedElement = getGson().toJsonTree(src);
        JsonObject serializedObject = serializedElement.getAsJsonObject();
        return serializedObject;
    }

    @Override
    public T deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context) throws JsonParseException {
        JsonObject jsonObject = json.getAsJsonObject();
        return getGson().fromJson(jsonObject, getImplementationTypeForDeserialization());
    }

    protected abstract Type getImplementationTypeForDeserialization();
}
