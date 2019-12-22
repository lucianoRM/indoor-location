package com.example.location.internal.entity.sensor;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.SensorContext;

import java.util.Map;

public class DefaultSensorContext implements SensorContext {

    private Map<String, SignalEmitter> signalEmitters;

    public DefaultSensorContext(Map<String, SignalEmitter> signalEmitters) {
        this.signalEmitters = signalEmitters;
    }

    @Override
    public Map<String, SignalEmitter> getSignalEmitters() {
        return this.signalEmitters;
    }
}
