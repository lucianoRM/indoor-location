package com.example.location.internal.entity.emitter;

import com.example.location.api.data.Position;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.entity.SkeletalIdentifiableObject;

import java.util.Map;
import java.util.Optional;

import static java.util.Collections.emptyMap;
import static java.util.Optional.empty;

public class DefaultSignalEmitter extends SkeletalIdentifiableObject implements SignalEmitter {

    public DefaultSignalEmitter(String id, String name, Position position) {
        super(id, name, position);
    }

    @Override
    public Optional<Float> getPower() {
        return empty();
    }

    @Override
    public Map<String, String> getAttributes() {
        return emptyMap();
    }

    @Override
    public void emitSignal() {

    }
}
