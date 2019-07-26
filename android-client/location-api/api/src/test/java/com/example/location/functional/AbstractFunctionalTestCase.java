package com.example.location.functional;

import com.example.location.api.system.EmitterManager;
import com.example.location.api.system.Locator;
import com.example.location.api.system.SensorManager;
import com.example.location.internal.config.SystemConfiguration;
import com.example.location.internal.config.LANSystemConfiguration;
import com.example.location.internal.config.TestSystemConfiguration;
import com.example.location.internal.container.DaggerLocationSystemComponent;
import com.example.location.internal.container.HttpClientModule;
import com.example.location.internal.container.LocationSystemComponent;
import com.example.location.internal.container.SystemConfigurationModule;
import com.example.location.internal.http.HttpLocationClient;
import com.google.gson.Gson;

import org.junit.Before;

import okhttp3.OkHttpClient;

import static java.lang.String.format;

public abstract class AbstractFunctionalTestCase {

    protected static final String USER_ID = "test_user";
    private LocationSystemComponent locationSystemComponent;

    @Before
    public void setUp() throws Exception{
        this.locationSystemComponent = DaggerLocationSystemComponent
                .builder()
                .systemConfigurationModule(new SystemConfigurationModule(getSystemConfig()))
                .httpClientModule(new HttpClientModule(USER_ID))
                .build();
    }

    protected SystemConfiguration getSystemConfig() {
        return new TestSystemConfiguration();
    }

    protected SensorManager getSensorManager() {
        return locationSystemComponent.sensorManager();
    }

    protected EmitterManager getEmitterManager() {
        return locationSystemComponent.emitterManager();
    }

    protected Gson getGson() {
        return locationSystemComponent.gson();
    }

    protected OkHttpClient httpClient() {
        return this.locationSystemComponent.httpClient();
    }

    protected HttpLocationClient locationClient() {
        return this.locationSystemComponent.locationServiceClient();
    }

    protected Locator locator() {
        return this.locationSystemComponent.locator();
    }

    protected String getServerUrl() {
        String protocol = this.locationSystemComponent.systemConfiguration().getServerProtocol();
        String host = this.locationSystemComponent.systemConfiguration().getServerHost();
        int port = this.locationSystemComponent.systemConfiguration().getServerPort();
        return format("%s://%s:%d", protocol, host, port);
    }

}
