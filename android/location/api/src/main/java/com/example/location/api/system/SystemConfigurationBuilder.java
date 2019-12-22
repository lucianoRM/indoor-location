package com.example.location.api.system;

import com.example.location.internal.config.DefaultSystemConfigurationBuilder;

/**
 * Builder for {@link SystemConfiguration}
 */
public interface SystemConfigurationBuilder {

    static SystemConfigurationBuilder systemConfigurationBuilder() {
        return new DefaultSystemConfigurationBuilder();
    }

    /**
     * Configure the id that represents this user in the system
     * @param userId the user id
     * @return this builder;
     */
    SystemConfigurationBuilder withUserId(String userId);

    /**
     * Configure the ip where the server will be listening
     * @param serverIp the server ip
     * @return this builder;
     */
    SystemConfigurationBuilder withServerIp(String serverIp);

    /**
     * Configure the port where the server will be listening
     * @param serverPort the server port
     * @return this builder
     */
    SystemConfigurationBuilder withServerPort(int serverPort);

    /**
     * Configure any implementation attribute that will be needed later.
     * @param attributeKey the key to locate the attribute
     * @param attribute the attribute
     * @param <T> attribute type
     * @return this builder
     */
    <T> SystemConfigurationBuilder withCustomConfigAttribute(String attributeKey, T attribute);

    /**
     * Build the {@link SystemConfiguration} with the provided parameters
     * @return a {@link SystemConfiguration}
     */
    SystemConfiguration build();
}
