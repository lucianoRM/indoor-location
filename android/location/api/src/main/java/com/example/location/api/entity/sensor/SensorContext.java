package com.example.location.api.entity.sensor;

import com.example.location.api.entity.emitter.SignalEmitter;

import java.util.Map;

/**
 * Context with information available for {@link SensorDataTransformer}s to correctly
 * compute it's values
 */
public interface SensorContext {

    /**
     * @return all signal emitters from the server
     */
    Map<String, SignalEmitter> getSignalEmitters();

}
