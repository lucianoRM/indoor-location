package com.example.location.api.entity.emitter;

import com.example.location.internal.entity.IdentifiableObject;

public interface SignalEmitter extends IdentifiableObject {

    /**
     * Emits the signal that defines this signal emitter.
     */
    void emitSignal();

}
