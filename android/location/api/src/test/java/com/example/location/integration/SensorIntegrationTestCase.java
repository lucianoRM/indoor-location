package com.example.location.integration;

import com.example.location.api.entity.sensor.SensorDataTransformer;
import com.example.location.api.data.Position;
import com.example.location.api.data.RawSensorData;
import com.example.location.api.data.SensorData;
import com.example.location.api.data.Signal;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorConfiguration;
import com.example.location.api.entity.sensor.SensorFeed;
import com.example.location.api.system.SensorAlreadyExistsException;
import com.example.location.functional.StaticSensorFeed;
import com.example.location.internal.entity.emitter.DefaultSignalEmitter;

import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;

import java.util.ArrayList;
import java.util.List;

import static com.example.location.NumberMatcher.closeTo;
import static com.example.location.api.entity.sensor.SensorConfiguration.sensorConfigurationBuilder;
import static java.lang.Long.parseLong;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.junit.rules.ExpectedException.none;

public class SensorIntegrationTestCase extends AbstractIntegrationTestCase {

    @Rule
    public ExpectedException expectedException = none();

    @Test
    public void createSensorIsSuccessful() throws Exception {
        final SensorFeed feed = new StaticSensorFeed();
        Sensor createdSensor = getSensorManager().createSensor(sensorConfigurationBuilder()
                .withId("id")
                .withName("name")
                .withFeed(feed)
                .withTransformer((s,d) -> new SensorData(0,0))
                .build());
        Sensor sensorInServer = getSensorFromServer(createdSensor.getId());
        assertThat(createdSensor, equalTo(sensorInServer));
    }

    @Test
    public void getOrCrateSensorIsSuccessful() throws Exception {
        final SensorFeed feed = new StaticSensorFeed();
        final String sensorId = "id";
        Sensor createdSensor = getSensorManager().getOrCreateSensor(sensorConfigurationBuilder()
                .withId(sensorId)
                .withName("name")
                .withFeed(feed)
                .withTransformer((s,d) -> new SensorData(0,0))
                .build());
        Sensor sensorInServer = getSensorFromServer(createdSensor.getId());
        assertThat(createdSensor, equalTo(sensorInServer));
    }

    @Test
    public void createAlreadyExistentSensor() throws Exception {
        final SensorFeed feed = new StaticSensorFeed();
        SensorConfiguration config = sensorConfigurationBuilder()
                .withId("id")
                .withName("name")
                .withFeed(feed)
                .withTransformer((s, d) -> new SensorData(0,0))
                .build();

        //Register one time
        getSensorManager().createSensor(config);

        expectedException.expect(SensorAlreadyExistsException.class);
        getSensorManager().createSensor(config);
    }

    @Test
    public void createAndGetAnExistentSensor() throws Exception {
        final String sensorId = "id";
        final SensorFeed feed = new StaticSensorFeed();
        SensorConfiguration config = sensorConfigurationBuilder()
                .withId(sensorId)
                .withName("name")
                .withFeed(feed)
                .withTransformer((s, d) -> new SensorData(0,0))
                .build();
        Sensor createdSensor = getSensorManager().createSensor(config);
        Sensor retrievedSensor = getSensorManager().getOrCreateSensor(config);
        assertThat(createdSensor, equalTo(retrievedSensor));
    }

    @Test
    public void sensorSenseUpdatesPosition() throws Exception {
        final String signalDistanceKey = "distance";
        final Signal signal = new Signal();
        signal.addAttribute(signalDistanceKey, "5");

        final String anchor1Id = "a1";
        final String se1id = "se1";
        final String se1Name = "SE1";
        final Position position1 = new Position(0, 0);

        final String anchor2Id = "a2";
        final String se2id = "se2";
        final String se2Name = "SE2";
        final Position position2 = new Position(10, 0);

        final String anchor3Id = "a3";
        final String se3id = "se3";
        final String se3Name = "SE3";
        final Position position3 = new Position(5, 5);

        registerAnchorInServer(createAnchor(anchor1Id, position1));
        SignalEmitter signalEmitter1 = new DefaultSignalEmitter(se1id, se1Name, signal);
        registerSignalEmitterInAnchor(anchor1Id, signalEmitter1);

        registerAnchorInServer(createAnchor(anchor2Id, position2));
        SignalEmitter signalEmitter2 = new DefaultSignalEmitter(se2id, se2Name, signal);
        registerSignalEmitterInAnchor(anchor2Id, signalEmitter2);

        registerAnchorInServer(createAnchor(anchor3Id, position3));
        SignalEmitter signalEmitter3 = new DefaultSignalEmitter(se3id, se3Name, signal);
        registerSignalEmitterInAnchor(anchor3Id, signalEmitter3);


        final StaticSensorFeed feed = new StaticSensorFeed();
        final SensorDataTransformer transformer = (d, c) ->
                //Here we should do a computation based on the sensed data and the signal being emitted. This is easier
                new SensorData(parseLong(c.getSignalEmitters().get(d.getEmitterId()).getSignal().getAttribute(signalDistanceKey).get()), 0);
        Sensor createdSensor = getSensorManager().createSensor(sensorConfigurationBuilder()
                .withId("id")
                .withName("name")
                .withFeed(feed)
                .withTransformer(transformer)
                .build());

        Position myPosition = findMe();
        assertThat(myPosition.getX(), equalTo(0.0f));
        assertThat(myPosition.getY(), equalTo(0.0f));

        List<RawSensorData> rawSensorData = new ArrayList<>();
        rawSensorData.add(new RawSensorData(se1id));
        rawSensorData.add(new RawSensorData(se2id));
        rawSensorData.add(new RawSensorData(se3id));
        feed.setData(rawSensorData);
        createdSensor.sense();
        myPosition = findMe();
        assertThat(myPosition.getX(), closeTo(5.0f));
        assertThat(myPosition.getY(), closeTo(0.57f));

    }
}
