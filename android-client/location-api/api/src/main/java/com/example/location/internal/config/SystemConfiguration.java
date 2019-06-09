package com.example.location.internal.config;

/**
 * Provides all configurable values in the system
 */
public interface SystemConfiguration {

    /**
     * @return The URL where the server is hosted.
     */
    String getServerUrl();

    /**
     * @return The port where the server is listening
     */
    int getServerPort();

}
