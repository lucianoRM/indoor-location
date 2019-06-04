package com.example.location.api.system;

import com.example.location.api.entity.emitter.SignalEmitter;

import java.util.Optional;

/**
 * Handles registrations and available {@link com.example.location.api.entity.emitter.SignalEmitter}s in the System
 */
public interface EmitterManager {

    /**
     * Gets the {@link SignalEmitter} associated with this id
     * @param id the id for the signal emmiter.
     * @return an {@link Optional<SignalEmitter>} if it exists or {@link Optional#empty()}
     */
    Optional<SignalEmitter> getSignalEmitter(String id);


}
