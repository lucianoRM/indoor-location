package com.example.location.internal.config;

public class ConfigurableSystemConfiguration implements SystemConfiguration {

    private String host;
    private int port;

    public ConfigurableSystemConfiguration(String host, int port) {
        this.host = host;
        this.port = port;
    }

    @Override
    public String getServerHost() {
        return host;
    }

    @Override
    public int getServerPort() {
        return port;
    }

    @Override
    public String getServerProtocol() {
        return "http";
    }
}
