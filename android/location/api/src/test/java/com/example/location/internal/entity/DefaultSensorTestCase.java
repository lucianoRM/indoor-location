package com.example.location.internal.entity;

import com.example.location.api.entity.sensor.SensorDataTransformer;
import com.example.location.api.data.RawSensorData;
import com.example.location.api.data.SensorData;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.system.EmitterManager;
import com.example.location.internal.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorFeed;
import com.example.location.internal.entity.sensor.DefaultSensor;
import com.example.location.internal.entity.sensor.SensorListener;

import org.junit.Test;
import org.mockito.ArgumentCaptor;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static java.lang.Thread.sleep;
import static java.util.concurrent.Executors.newSingleThreadExecutor;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.mockito.ArgumentCaptor.forClass;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static java.util.Optional.of;

public class DefaultSensorTestCase {

    @Test
    public void sensorGetsObjectsFromFeed() throws Exception{
        SensorFeed sensorFeed = mock(SensorFeed.class);
        SensorDataTransformer dataTransformer = mock(SensorDataTransformer.class);
        SensorListener sensorListener = mock(SensorListener.class);
        EmitterManager emitterManager = mock(EmitterManager.class);

        final String emitterId1 = "e1";
        final String emitterId2 = "e2";
        final SignalEmitter se1 = mock(SignalEmitter.class);
        final SignalEmitter se2 = mock(SignalEmitter.class);
        when(se1.getId()).thenReturn(emitterId1);
        when(se2.getId()).thenReturn(emitterId2);

        List<RawSensorData> sensedDataList = new ArrayList<>();
        sensedDataList.add(new RawSensorData(emitterId1));
        sensedDataList.add(new RawSensorData(emitterId2));
        when(sensorFeed.getData()).thenReturn(sensedDataList);

        List<SensorData> transformedData = new ArrayList<>();
        transformedData.add(new SensorData(0.0f, 0L));
        transformedData.add(new SensorData(0.0f, 0L));
        when(dataTransformer.transform(eq(sensedDataList.get(0)),any())).thenReturn(transformedData.get(0));
        when(dataTransformer.transform(eq(sensedDataList.get(1)),any())).thenReturn(transformedData.get(1));

        Map<String, SignalEmitter> signalEmitters = new HashMap<>();
        signalEmitters.put(emitterId1, se1);
        signalEmitters.put(emitterId2, se2);
        when(emitterManager.getSignalEmitters()).thenReturn(signalEmitters);

        Sensor sensor = new DefaultSensor(
                "id",
                "name",
                sensorFeed,
                dataTransformer,
                sensorListener,
                emitterManager);

        sensor.sense();

        ArgumentCaptor<List<SensedObject>> objectsCaptor = forClass(List.class);
        verify(sensorListener).onSensorUpdate(eq(sensor), objectsCaptor.capture());

        List<SensedObject> capturedList = objectsCaptor.getValue();
        assertThat(capturedList.get(0).getData(), equalTo(transformedData.get(0)));
        assertThat(capturedList.get(1).getData(), equalTo(transformedData.get(1)));
    }
}
