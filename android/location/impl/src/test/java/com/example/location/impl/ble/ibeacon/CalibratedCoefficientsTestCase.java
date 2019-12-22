package com.example.location.impl.ble.ibeacon;

import com.example.location.api.data.RawSensorData;
import com.example.location.api.data.Signal;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.SensorContext;

import org.junit.Before;
import org.junit.Test;


import java.util.HashMap;
import java.util.Map;

import static com.example.location.impl.RadioDataTransformer.MEDIUM_COEFFICIENT_SIGNAL_KEY;
import static java.lang.Float.parseFloat;
import static java.util.Optional.empty;
import static java.util.Optional.of;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class CalibratedCoefficientsTestCase {

    private static final float DEFAULT_COEFF = 4.0f;

    private IBeaconDataTransformer dataTransformer = new IBeaconDataTransformer();

    private SignalEmitter mockedSignalEmitter;
    private RawSensorData mockedSensorData;
    private SensorContext mockedSensorContext;
    private Signal mockedSignal;

    private Map<String, SignalEmitter> allEmitters;

    @Before
    public void setUp() {
        final String emitterId = "emitter";

        mockedSignal = mock(Signal.class);
        mockedSignalEmitter = mock(SignalEmitter.class);
        mockedSensorData = mock(RawSensorData.class);
        mockedSensorContext = mock(SensorContext.class);

        when(mockedSensorData.getEmitterId()).thenReturn(emitterId);

        when(mockedSignal.getAttribute(anyString())).thenReturn(empty());
        when(mockedSignalEmitter.getSignal()).thenReturn(mockedSignal);

        allEmitters = new HashMap<>();
        allEmitters.put(emitterId, mockedSignalEmitter);

        when(mockedSensorContext.getSignalEmitters()).thenReturn(allEmitters);
    }

    @Test
    public void noSignalInformationGivesDefaultValues() {
        assertThat(dataTransformer.getMediumCoef(mockedSensorData, mockedSensorContext), equalTo(DEFAULT_COEFF));
    }

    @Test
    public void serverCoefIfPopulated() {
        final String newCoeff = "3.14";
        when(mockedSignal.getAttribute(MEDIUM_COEFFICIENT_SIGNAL_KEY)).thenReturn(of(newCoeff));
        assertThat(dataTransformer.getMediumCoef(mockedSensorData, mockedSensorContext), equalTo(parseFloat(newCoeff)));
    }

    @Test
    public void calibratedCoeffsReturnedIfAvailable() {
        Map<String, Float> beacons = new HashMap<>();
        beacons.put("1", 10.0f);
        beacons.put("2", 20.0f);
        beacons.put("3", 30.0f);
        allEmitters.put("1", mock(SignalEmitter.class));
        allEmitters.put("2", mock(SignalEmitter.class));
        allEmitters.put("3", mock(SignalEmitter.class));
        beacons.forEach((k,v) -> when(mockedSignal.getAttribute(buildCoeffKey(k))).thenReturn(of(v.toString())));
        assertThat(dataTransformer.getMediumCoef(mockedSensorData, mockedSensorContext), equalTo(20.0f));
    }

    @Test
    public void zeroValueCoeffsAreNotTakenIntoAccount() {
        Map<String, Float> beacons = new HashMap<>();
        beacons.put("1", 10.0f);
        beacons.put("2", 20.0f);
        beacons.put("3", 30.0f);
        for(int i = 4; i < 100 ; i++) {
            beacons.put(Integer.toString(i), 0.0f);
        }
        allEmitters.put("1", mock(SignalEmitter.class));
        allEmitters.put("2", mock(SignalEmitter.class));
        allEmitters.put("3", mock(SignalEmitter.class));
        beacons.forEach((k,v) -> when(mockedSignal.getAttribute(buildCoeffKey(k))).thenReturn(of(v.toString())));
        assertThat(dataTransformer.getMediumCoef(mockedSensorData, mockedSensorContext), equalTo(20.0f));
    }

    @Test
    public void coeffsNotInSignalNotTakenIntoAccount() {
        final String iBeacon = "3";
        final float iBeaconCoeff = 30.0f;
        Map<String, Float> beacons = new HashMap<>();
        beacons.put("1", 10.0f);
        beacons.put("2", 20.0f);
        beacons.put(iBeacon, iBeaconCoeff);
        allEmitters.put("1", mock(SignalEmitter.class));
        allEmitters.put("2", mock(SignalEmitter.class));
        allEmitters.put("3", mock(SignalEmitter.class));
        when(mockedSignal.getAttribute(buildCoeffKey(iBeacon))).thenReturn(of(Float.toString(iBeaconCoeff)));
        assertThat(dataTransformer.getMediumCoef(mockedSensorData, mockedSensorContext), equalTo(30.0f));
    }

    private String buildCoeffKey(String id) {
        return "MEDIUM_COEF_BY_" + id;
    }

}
