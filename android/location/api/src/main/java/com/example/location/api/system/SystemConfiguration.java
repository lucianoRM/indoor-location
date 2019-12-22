package com.example.location.api.system;

/**
 * Provides all configurable values in the system
 */
public interface SystemConfiguration {

    /**
     * @return The id of this user in the server
     */
    String getUserId();

    /**
     * @return The URL where the server is hosted.
     */
    String getServerHost();

    /**
     * @return The port where the server is listening
     */
    int getServerPort();

    /**
     * @return The protocol used by the server
     */
    default String getServerProtocol() {
        return "http";
    }

    /**
     * @return An specific, implentation aware attribute.
     */
    <T> T getConfigAttribute(String attributeKey);

}
