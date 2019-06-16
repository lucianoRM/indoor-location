package com.example.location.internal.serialization;

import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import com.google.gson.JsonSerializationContext;

import java.lang.reflect.Type;

public abstract class TypedObjectSerializer<T> extends DelegatingSerializer<T> {

    private static final String TYPE_KEY = "type";

    @Override
    public JsonElement serialize(T src, Type typeOfSrc, JsonSerializationContext context) {
        JsonElement serializedElement = getGson().toJsonTree(src);
        JsonObject serializedObject = serializedElement.getAsJsonObject();
        serializedObject.addProperty(TYPE_KEY, getTypeForSerialization(src));
        return serializedObject;
    }

    @Override
    public T deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context) throws JsonParseException {
        JsonObject jsonObject = json.getAsJsonObject();
        String type = jsonObject.get(TYPE_KEY).getAsString();
        return getGson().fromJson(jsonObject, getImplementationTypeForDeserialization(type));
    }

    protected abstract Type getImplementationTypeForDeserialization(String type);

    protected abstract String getTypeForSerialization(T object);

}
