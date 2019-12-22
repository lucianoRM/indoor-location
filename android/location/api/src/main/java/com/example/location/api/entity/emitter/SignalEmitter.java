package com.example.location.api.entity.emitter;

import com.example.location.api.data.Signal;
import com.example.location.internal.entity.IdentifiableObject;
import com.example.location.internal.entity.sensor.PositionableObject;

public interface SignalEmitter extends IdentifiableObject,PositionableObject {

    /**
     * @return the {@link Signal} being emitted by this {@link SignalEmitter}
     */
    Signal getSignal();

    /**
     * Emits the signal that defines this signal emitter.
     */
    void emitSignal();

}
