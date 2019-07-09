package com.example.location.api.system;

import com.example.location.internal.config.LANSystemConfiguration;
import com.example.location.internal.container.DaggerLocationSystemComponent;
import com.example.location.internal.container.HttpClientModule;
import com.example.location.internal.container.LocationSystemComponent;
import com.example.location.internal.container.SystemConfigurationModule;

public final class LocationSystem {

    private LocationSystemComponent locationSystemComponent;

    public LocationSystem(String userId) {
        this.locationSystemComponent = DaggerLocationSystemComponent
                .builder()
                .systemConfigurationModule(new SystemConfigurationModule(new LANSystemConfiguration()))
                .httpClientModule(new HttpClientModule(userId))
                .build();
    }

    public SensorManager getSensorManager() {
        return locationSystemComponent.sensorManager();
    }

    public EmitterManager getEmitterManager() {
        return locationSystemComponent.emitterManager();
    }
}
