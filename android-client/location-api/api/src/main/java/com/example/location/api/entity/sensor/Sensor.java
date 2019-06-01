package com.example.location.api.entity.sensor;

import com.example.location.internal.entity.IdentifiableObject;

public interface Sensor extends IdentifiableObject {

    /**
     * Execute this {@link Sensor} sensing action
     */
    void sense();

}
