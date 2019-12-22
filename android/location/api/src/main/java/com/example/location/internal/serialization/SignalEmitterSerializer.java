package com.example.location.internal.serialization;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.entity.emitter.SignalEmitterView;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import com.google.gson.JsonSerializationContext;

import java.lang.reflect.Type;

public class SignalEmitterSerializer extends InterfaceSerializer<SignalEmitter> {


    @Override
    public JsonElement serialize(SignalEmitter src, Type typeOfSrc, JsonSerializationContext context) {
        JsonElement serializedSignalEmitter = super.serialize(src, typeOfSrc, context);
        JsonObject seObject = serializedSignalEmitter.getAsJsonObject();
        JsonObject signalObject = seObject.get("signal").getAsJsonObject();
        JsonElement signalAttributes = signalObject.get("attributes");
        seObject.add("signal", signalAttributes);
        return seObject;
    }

    @Override
    public SignalEmitter deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context) throws JsonParseException {
        JsonObject signalEmitter = json.getAsJsonObject();
        JsonElement signalAttributes = signalEmitter.get("signal");
        JsonObject signal = new JsonObject();
        signal.add("attributes", signalAttributes);
        signalEmitter.add("signal", signal);
        return super.deserialize(signalEmitter, typeOfT, context);
    }

    @Override
    protected Type getImplementationTypeForDeserialization() {
        return SignalEmitterView.class;
    }

}
