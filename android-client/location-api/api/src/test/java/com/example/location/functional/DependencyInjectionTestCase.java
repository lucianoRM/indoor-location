package com.example.location.functional;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorFeed;

import org.junit.Test;

import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.RecordedRequest;

import static com.example.location.api.entity.sensor.SensorConfiguration.sensorConfigurationBuilder;
import static org.hamcrest.CoreMatchers.containsString;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.mockito.Mockito.mock;

public class DependencyInjectionTestCase extends AbstractFunctionalTestCase {

    @Test
    public void test() throws Exception{
        final SensorFeed sensorFeed = mock(SensorFeed.class);
        getMockedServer().enqueue(new MockResponse().setBody("[]"));
        RecordedRequest request =  getMockedServer().takeRequest();
        Sensor sensor = getContainer().sensorManager().createSensor(
                sensorConfigurationBuilder()
                        .withId("a")
                        .withName("b")
                        .withFeed(sensorFeed)
                        .build()
        );
        sensor.sense();
        assertThat(request.getPath(), containsString("signal_emitters"));
    }

}
