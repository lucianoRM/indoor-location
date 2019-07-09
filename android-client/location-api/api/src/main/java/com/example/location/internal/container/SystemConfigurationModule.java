package com.example.location.internal.container;

import com.example.location.internal.config.SystemConfiguration;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;

@Module
public class SystemConfigurationModule {

    private SystemConfiguration config;

    public SystemConfigurationModule(SystemConfiguration systemConfiguration) {
        this.config = systemConfiguration;
    }

    @Singleton
    @Provides
    public SystemConfiguration systemConfiguration() {
        return this.config;
    }

}
