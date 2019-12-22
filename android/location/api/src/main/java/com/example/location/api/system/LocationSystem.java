package com.example.location.api.system;

import com.example.location.internal.container.DaggerLocationSystemComponent;
import com.example.location.internal.container.HttpClientModule;
import com.example.location.internal.container.LocationSystemComponent;
import com.example.location.internal.container.SystemConfigurationModule;
import com.example.location.internal.logger.ServerLogger;

public final class LocationSystem {

    private LocationSystemComponent locationSystemComponent;

    public LocationSystem(SystemConfiguration systemConfiguration) {
        this.locationSystemComponent = DaggerLocationSystemComponent
                .builder()
                .systemConfigurationModule(new SystemConfigurationModule(systemConfiguration))
                .httpClientModule(new HttpClientModule(systemConfiguration.getUserId()))
                .build();
    }

    public SensorManager getSensorManager() {
        return locationSystemComponent.sensorManager();
    }

    public EmitterManager getEmitterManager() {
        return locationSystemComponent.emitterManager();
    }

    public Locator getLocator() {
        return locationSystemComponent.locator();
    }

    public ServerLogger getServerLogger() {
        return locationSystemComponent.serverLogger();
    }
}
