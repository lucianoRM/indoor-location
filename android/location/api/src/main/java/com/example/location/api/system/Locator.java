package com.example.location.api.system;

import com.example.location.api.data.Position;

/**
 * Locates the uses within the system
 */
public interface Locator {

    /**
     * Gets the position of the user
     * @return the {@link Position} of the user
     */
    Position getPosition() throws LocatorException;

}
