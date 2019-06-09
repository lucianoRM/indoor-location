package com.example.location.integration;

import com.example.location.api.data.DataTransformer;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.entity.sensor.SensorFeed;
import com.example.location.api.system.SensorAlreadyExistsException;
import com.example.location.functional.StaticSensorFeed;
import com.example.location.functional.TestDataTransformer;

import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;

import static com.example.location.api.entity.sensor.SensorConfiguration.sensorConfigurationBuilder;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.junit.rules.ExpectedException.none;

public class SensorManagerTestCase extends AbstractIntegrationTestCase {

    @Rule
    public ExpectedException expectedException = none();

    @Test
    public void createSensorIsSuccessful() throws Exception {
        final SensorFeed feed = new StaticSensorFeed();
        final DataTransformer transformer = new TestDataTransformer();
        Sensor createdSensor = getContainer().sensorManager().createSensor(sensorConfigurationBuilder()
                .withId("id")
                .withName("name")
                .withFeed(feed)
                .withTransformer(transformer)
                .build());
        Sensor sensorInServer = getSensorFromServer(createdSensor.getId());
        assertThat(createdSensor, equalTo(sensorInServer));
    }

    @Test
    public void createAlreadyExistentSensor() throws Exception {
        final SensorFeed feed = new StaticSensorFeed();
        final DataTransformer transformer = new TestDataTransformer();
        SensorConfiguration config = sensorConfigurationBuilder()
                .withId("id")
                .withName("name")
                .withFeed(feed)
                .withTransformer(transformer)
                .build();

        //Register one time
        getContainer().sensorManager().createSensor(config);

        expectedException.expect(SensorAlreadyExistsException.class);
        getContainer().sensorManager().createSensor(config);
    }
}
