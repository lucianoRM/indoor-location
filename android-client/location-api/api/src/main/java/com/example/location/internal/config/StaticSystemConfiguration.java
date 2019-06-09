package com.example.location.internal.config;

public class StaticSystemConfiguration implements SystemConfiguration{

    private static final SystemConfiguration singleton = new StaticSystemConfiguration();

    private StaticSystemConfiguration() {}

    public static SystemConfiguration config() {
        return singleton;
    }

    @Override
    public String getServerUrl() {
        return "http://localhost";
    }

    @Override
    public int getServerPort() {
        return 5000;
    }
}
