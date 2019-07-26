package com.example.location.api.system;

import com.example.location.api.data.Position;

/**
 * Locates the uses within the system
 */
public interface Locator {

    /**
     * @return the position of the user
     */
    Position getPosition();

}
