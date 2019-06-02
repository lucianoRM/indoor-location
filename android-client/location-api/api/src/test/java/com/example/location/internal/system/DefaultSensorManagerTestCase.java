package com.example.location.internal.system;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.entity.sensor.SensorFeed;
import com.example.location.internal.http.HttpLocationClient;

import org.junit.Test;

import static com.example.location.api.entity.sensor.SensorConfiguration.sensorConfigurationBuilder;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.mockito.Mockito.mock;

public class DefaultSensorManagerTestCase {

    private HttpLocationClient httpLocationClient = mock(HttpLocationClient.class);
    private DefaultSensorManager sensorManager = new DefaultSensorManager(httpLocationClient);

    @Test
    public void createsSensorFromConfigWithExtraArgs() {
        final String sensorId = "sensorId";
        final String sensorName = "sensorName";
        final SensorFeed mockedFeed = mock(SensorFeed.class);
        SensorConfiguration sensorConfiguration = sensorConfigurationBuilder()
                .withId(sensorId)
                .withName(sensorName)
                .withFeed(mockedFeed)
                .build();
        Sensor sensor = sensorManager.createSensor(sensorConfiguration);
        assertThat(sensor.getId(), equalTo(sensorId));
        assertThat(sensor.getName(), equalTo(sensorName));
    }

}
