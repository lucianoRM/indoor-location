package com.example.location.api.entity.emitter;

import com.example.location.internal.entity.IdentifiableObject;

import java.util.Map;
import java.util.Optional;

public interface SignalEmitter extends IdentifiableObject {

    /**
     * @return the power with which this {@link SignalEmitter} is sending it's signal.
     */
    Optional<Float> getPower();

    /**
     * Attributes specific to some {@link SignalEmitter} implementation. If none, return an empty map.
     * @return a {@link Map<String,String>} containing special attributes that define this {@link SignalEmitter}
     */
    Map<String, String> getAttributes();

    /**
     * Emits the signal that defines this signal emitter.
     */
    void emitSignal();

}
