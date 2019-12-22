package com.example.location.functional;


import com.example.location.api.data.RawSensorData;
import com.example.location.api.data.SensorData;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorFeed;

import org.junit.Test;

import java.util.List;

import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.RecordedRequest;

import static com.example.location.JsonMatcher.sameJson;
import static com.example.location.TestUtils.readFile;
import static com.example.location.api.entity.sensor.SensorConfiguration.sensorConfigurationBuilder;
import static java.util.Collections.singletonList;
import static org.hamcrest.CoreMatchers.containsString;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;

public class SensingServerSynchronizationTestCase extends MockedServerFunctionalTestCase {

    private static final String SENSOR_JSON = "sensor.json";
    private static final String EMITTER_JSON = "signal_emitter.json";

    @Test
    public void sensingSensorUpdatesValuesInServer() throws Exception{
        final String serializedSensor = readFile(SENSOR_JSON);
        //Just to prevent failing due to wrong serialization
        getMockedServer().enqueue(new MockResponse().setBody(serializedSensor));

        final StaticSensorFeed feed = new StaticSensorFeed();

        Sensor createdSensor = getSensorManager().createSensor(
                sensorConfigurationBuilder()
                        .withId("id")
                        .withFeed(feed)
                        .withTransformer((s,d) -> new SensorData(0,0))
                        .build());
        getMockedServer().takeRequest(); //create sensor request

        String serializedSignalEmitter = readFile(EMITTER_JSON);
        List<SignalEmitter> signalEmitters = singletonList(getGson().fromJson(serializedSignalEmitter, SignalEmitter.class));

        final RawSensorData rawData = new RawSensorData(signalEmitters.get(0).getId());
        feed.setData(singletonList(rawData));

        //For when the sensor checks for the signalEmitter
        getMockedServer().enqueue(new MockResponse().setBody("[" + serializedSignalEmitter + "]"));

        getMockedServer().enqueue(new MockResponse().setBody("sensor updated"));

        createdSensor.sense();

        RecordedRequest getSignalEmitterRequest = getMockedServer().takeRequest();
        assertThat(getSignalEmitterRequest.getPath(), containsString("signal_emitters"));

        RecordedRequest updateSensorRequest = getMockedServer().takeRequest();
        assertThat(updateSensorRequest.getPath(), containsString("sensors/" + createdSensor.getId()));
        String requestBody = updateSensorRequest.getBody().readUtf8();
        assertThat(requestBody, containsString("\"id\":\"" + signalEmitters.get(0).getId()));
        assertThat(requestBody, containsString("\"data\":{"));
    }

    @Test
    public void sensorCreationUpdatesServer() throws Exception{
        final SensorFeed feed = new StaticSensorFeed();
        String serializedSensor = readFile(SENSOR_JSON);
        Sensor expectedSensor = getGson().fromJson(serializedSensor, Sensor.class);

        getMockedServer().enqueue(new MockResponse().setBody(serializedSensor));

        Sensor createdSensor = getSensorManager().createSensor(
                sensorConfigurationBuilder()
                        .withId(expectedSensor.getId())
                        .withName(expectedSensor.getName())
                        .withFeed(feed)
                        .withTransformer((s,d) -> new SensorData(0,0))
                        .build());

        assertThat(createdSensor, equalTo(expectedSensor));

        RecordedRequest request = getMockedServer().takeRequest();
        assertThat(request.getBody().readUtf8(), sameJson(serializedSensor));
        assertThat(request.getPath(), containsString("sensors"));
    }

}
