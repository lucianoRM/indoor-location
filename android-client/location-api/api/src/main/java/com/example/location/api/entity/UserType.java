package com.example.location.api.entity;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.Sensor;

public enum UserType {

    /**
     * An user that is also a {@link Sensor}
     */
    SENSOR,

    /**
     * An user that is also a {@link SignalEmitter}
     */
    ANCHOR

}
