package com.example.location.internal.entity.sensor;

import com.example.location.api.data.Position;

/**
 * Identifies an object that can be located in the system
 */
public interface PositionableObject {

    /**
     * @return the {@link Position} of the object
     */
    Position getPosition();
}
