package com.example.location.internal.system;

import com.example.location.api.data.DataTransformer;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.entity.sensor.SensorFeed;
import com.example.location.api.system.EmitterManager;
import com.example.location.internal.http.HttpLocationClient;

import org.junit.Before;
import org.junit.Test;

import javax.annotation.Nullable;

import okhttp3.MediaType;
import okhttp3.ResponseBody;
import okhttp3.internal.http.RealResponseBody;
import okio.BufferedSource;
import retrofit2.Call;

import static com.example.location.api.entity.sensor.SensorConfiguration.sensorConfigurationBuilder;
import static com.example.location.internal.http.HttpCode.NOT_FOUND;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static retrofit2.Response.error;
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

        Call<Sensor> registerSensorMockedCall = mock(Call.class);
        doReturn(success("")).when(registerSensorMockedCall).execute();
        when(mockedHttpClient.registerSensor(any())).thenReturn(registerSensorMockedCall);

        sensorManager = new DefaultSensorManager(mockedHttpClient, mockedEmitterManager);
    }

    private void configureMock(boolean isSensorInServer) throws Exception{
        Call<Sensor> getSensorMockedCall = mock(Call.class);
        if(isSensorInServer) {
            doReturn(success("")).when(getSensorMockedCall).execute();
        }else {
            doReturn(error(NOT_FOUND.code(), new ResponseBody() {
                @Nullable
                @Override
                public MediaType contentType() {
                    return null;
                }

                @Override
                public long contentLength() {
                    return 0;
                }

                @Override
                public BufferedSource source() {
                    return null;
                }
            })).when(getSensorMockedCall).execute();
        }
        when(mockedHttpClient.getSensor(any())).thenReturn(getSensorMockedCall);
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

    @Test
    public void getOrCreateSensorCreatesSensorIfNotFound() throws Exception {
        configureMock(false);
        final String sensorId = "sensorId";
        final String sensorName = "sensorName";
        SensorConfiguration sensorConfiguration = sensorConfigurationBuilder()
                .withId(sensorId)
                .withName(sensorName)
                .withFeed(mockedFeed)
                .withTransformer(mockedTransformer)
                .build();
        Sensor sensor = sensorManager.getOrCreateSensor(sensorId, sensorConfiguration);
        assertThat(sensor.getId(), equalTo(sensorId));
        assertThat(sensor.getName(), equalTo(sensorName));

        verify(mockedHttpClient, times(1)).registerSensor(eq(sensor));
    }

    @Test
    public void getOrCreateSensorReturnsSensorIfFound() throws Exception {
        configureMock(true);
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

        sensor = sensorManager.getOrCreateSensor(sensorId, sensorConfiguration);

        verify(mockedHttpClient, times(1)).registerSensor(eq(sensor));
    }

}
