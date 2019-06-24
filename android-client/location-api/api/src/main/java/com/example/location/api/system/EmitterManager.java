package com.example.location.api.system;

import com.example.location.api.entity.emitter.SignalEmitter;

import java.util.Optional;

/**
 * Handles registrations and available {@link com.example.location.api.entity.emitter.SignalEmitter}s in the LocationSystem
 */
public interface EmitterManager {

    /**
     * Register a new {@link SignalEmitter}
     * @param signalEmitter to be registered
     */
    void registerEmitter(SignalEmitter signalEmitter) throws EmitterManagerException;

    //TODO: Check if this should be public or it should be part of an internal interface
    /**
     * Gets the {@link SignalEmitter} associated with this id
     * @param id the id for the signal emmiter.
     * @return an {@link Optional<SignalEmitter>} if it exists or {@link Optional#empty()}
     */
    Optional<SignalEmitter> getSignalEmitter(String id) throws EmitterManagerException;


}
