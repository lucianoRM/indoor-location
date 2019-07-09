package com.example.location.internal.config;

public class TestSystemConfiguration implements SystemConfiguration{

    @Override
    public String getServerProtocol() {
        return "http";
    }

    @Override
    public String getServerHost() {
        return "localhost";
    }

    @Override
    public int getServerPort() {
        return 5000;
    }
}
