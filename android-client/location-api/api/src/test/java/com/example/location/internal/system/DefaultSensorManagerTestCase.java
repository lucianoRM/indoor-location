package com.example.location.internal.system;

import com.example.location.api.data.DataTransformer;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.entity.sensor.SensorFeed;
import com.example.location.api.system.EmitterManager;
import com.example.location.internal.http.HttpLocationClient;

import org.junit.Before;
import org.junit.Test;

import retrofit2.Call;

import static com.example.location.api.entity.sensor.SensorConfiguration.sensorConfigurationBuilder;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static retrofit2.Response.success;

public class DefaultSensorManagerTestCase {

    private HttpLocationClient mockedHttpClient;
    private EmitterManager mockedEmitterManager;
    private SensorFeed mockedFeed;
    private DataTransformer mockedTransformer;

    private DefaultSensorManager sensorManager;

    @Before
    public void setUp() throws Exception{
        mockedHttpClient = mock(HttpLocationClient.class);
        mockedEmitterManager = mock(EmitterManager.class);
        mockedFeed = mock(SensorFeed.class);
        mockedTransformer = mock(DataTransformer.class);

        Call<Sensor> mockedCall = mock(Call.class);
        doReturn(success("")).when(mockedCall).execute();
        when(mockedHttpClient.registerSensor(any())).thenReturn(mockedCall);

        sensorManager = new DefaultSensorManager(mockedHttpClient, mockedEmitterManager);
    }

    @Test
    public void createsSensorFromConfigWithExtraArgs() throws Exception{
        final String sensorId = "sensorId";
        final String sensorName = "sensorName";
        SensorConfiguration sensorConfiguration = sensorConfigurationBuilder()
                .withId(sensorId)
                .withName(sensorName)
                .withFeed(mockedFeed)
                .withTransformer(mockedTransformer)
                .build();
        Sensor sensor = sensorManager.createSensor(sensorConfiguration);
        assertThat(sensor.getId(), equalTo(sensorId));
        assertThat(sensor.getName(), equalTo(sensorName));
    }

    @Test
    public void sensorIsRegisteredAfterCreation() throws Exception{
        SensorConfiguration config = sensorConfigurationBuilder().withFeed(mockedFeed).withTransformer(mockedTransformer).build();
        Sensor sensor = sensorManager.createSensor(config);
        verify(mockedHttpClient, times(1)).registerSensor(eq(sensor));

    }

}
