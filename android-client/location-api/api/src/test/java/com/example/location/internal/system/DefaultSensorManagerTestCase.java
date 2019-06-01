package com.example.location.internal.system;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.entity.sensor.SensorFeed;

import org.junit.Test;

import static com.example.location.api.entity.sensor.SensorConfiguration.sensorConfigurationBuilder;
import static org.mockito.Mockito.mock;

public class DefaultSensorManagerTestCase {

    private DefaultSensorManager sensorManager = new DefaultSensorManager();

    @Test
    public void createNewSensor() {
        final String sensorId = "sensorId";
        final String sensorName = "sensorName";
        final SensorFeed mockedFeed = mock(SensorFeed.class);
        SensorConfiguration sensorConfiguration = sensorConfigurationBuilder()
                .withId(sensorId)
                .withName(sensorName)
                .withFeed(mockedFeed)
                .build();
        Sensor sensor = sensorManager.createSensor(sensorConfiguration);
    }

}
