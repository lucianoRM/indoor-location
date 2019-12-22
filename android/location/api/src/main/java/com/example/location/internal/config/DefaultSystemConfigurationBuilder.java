package com.example.location.internal.config;

import com.example.location.api.system.SystemConfiguration;
import com.example.location.api.system.SystemConfigurationBuilder;

import java.util.HashMap;
import java.util.Map;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;

public class DefaultSystemConfigurationBuilder implements SystemConfigurationBuilder {

    private String userId;
    private String serverIp;
    private int serverPort;
    private Map<String, Object> customAttributes = new HashMap<>();

    @Override
    public SystemConfigurationBuilder withUserId(String userId) {
        this.userId = userId;
        return this;
    }

    @Override
    public SystemConfigurationBuilder withServerIp(String serverIp) {
        this.serverIp = serverIp;
        return this;
    }

    @Override
    public SystemConfigurationBuilder withServerPort(int serverPort) {
        this.serverPort = serverPort;
        return this;
    }

    @Override
    public SystemConfigurationBuilder withCustomConfigAttribute(String attributeKey, Object attribute) {
        this.customAttributes.put(attributeKey, attribute);
        return this;
    }

    @Override
    public SystemConfiguration build() {
        checkNotNull(serverIp, "User ID should be configured");
        checkNotNull(serverIp, "Server IP should be configured");
        checkArgument(serverPort != 0, "Server port should be configured");
        return new InternalSystemConfigurationImplementation(userId,serverIp, serverPort, customAttributes);
    }

    private static class InternalSystemConfigurationImplementation implements SystemConfiguration {

        private String userId;
        private String serverIp;
        private int serverPort;
        private Map<String, Object> customAttributes;

        public InternalSystemConfigurationImplementation(String userId,
                                                         String serverIp,
                                                         int serverPort,
                                                         Map<String, Object> customAttributes) {
            this.userId = userId;
            this.serverIp = serverIp;
            this.serverPort = serverPort;
            this.customAttributes = new HashMap<>(customAttributes);
        }

        @Override
        public String getUserId() {
            return this.userId;
        }

        @Override
        public String getServerHost() {
            return this.serverIp;
        }

        @Override
        public int getServerPort() {
            return this.serverPort;
        }

        @Override
        public <T> T getConfigAttribute(String attributeKey) {
            return (T) customAttributes.get(attributeKey);
        }
    }
}
