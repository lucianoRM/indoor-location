package com.example.location.api.sensor;

import com.example.location.api.entity.sensor.SensorDataTransformer;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.entity.sensor.SensorFeed;

import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;

import static com.example.location.api.entity.sensor.SensorConfiguration.sensorConfigurationBuilder;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.CoreMatchers.notNullValue;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.IsNot.not;
import static org.junit.rules.ExpectedException.none;
import static org.mockito.Mockito.mock;

public class SensorConfigurationTestCase {

    private static final SensorFeed sensorFeed = mock(SensorFeed.class);
    private static final SensorDataTransformer dataTransformer = mock(SensorDataTransformer.class);
    private static final String sensorId = "sensorId";
    private static final String sensorName = "sensorName";

    @Rule
    public ExpectedException expectedException = none();

    @Test
    public void simpleConfiguration() {
        SensorConfiguration sensorConfiguration = sensorConfigurationBuilder()
                .withId(sensorId)
                .withName(sensorName)
                .withFeed(sensorFeed)
                .withTransformer(dataTransformer)
                .build();
        assertThat(sensorConfiguration.getSensorId(), equalTo(sensorId));
        assertThat(sensorConfiguration.getSensorName(), equalTo(sensorName));
        assertThat(sensorConfiguration.getSensorFeed(), equalTo(sensorFeed));
        assertThat(sensorConfiguration.getDataTransformer(), equalTo(dataTransformer));
    }

    @Test
    public void builderFailsIfNoFeed() {
        expectedException.expect(IllegalArgumentException.class);
        expectedException.expectMessage("Can't create a Sensor without a SensorFeed");
        sensorConfigurationBuilder().withId(sensorId).withName(sensorName).withTransformer(dataTransformer).build();
    }

    @Test
    public void builderFailsIfNoTransformer() {
        expectedException.expect(IllegalArgumentException.class);
        expectedException.expectMessage("Need to configure a SensorDataTransformer for the Sensor");
        sensorConfigurationBuilder().withId(sensorId).withName(sensorName).withFeed(sensorFeed).build();
    }

    @Test
    public void nameIsIdByDefault() {
        SensorConfiguration sensorConfiguration = sensorConfigurationBuilder()
                .withId(sensorId)
                .withFeed(sensorFeed)
                .withTransformer(dataTransformer)
                .build();
        assertThat(sensorConfiguration.getSensorName(), equalTo(sensorId));
    }

    @Test
    public void idIsAutogeneratedIfNotGiven() {
        SensorConfiguration sensorConfiguration1 = sensorConfigurationBuilder()
                .withFeed(sensorFeed)
                .withTransformer(dataTransformer)
                .build();
        SensorConfiguration sensorConfiguration2 = sensorConfigurationBuilder()
                .withFeed(sensorFeed)
                .withTransformer(dataTransformer)
                .build();
        assertThat(sensorConfiguration1.getSensorId(), notNullValue());
        assertThat(sensorConfiguration2.getSensorId(), notNullValue());
        assertThat(sensorConfiguration1.getSensorId(), is(equalTo(sensorConfiguration1.getSensorName())));
        assertThat(sensorConfiguration2.getSensorId(), is(equalTo(sensorConfiguration2.getSensorName())));
        assertThat(sensorConfiguration1.getSensorId(), is(not(equalTo(sensorConfiguration2.getSensorId()))));
    }


}
