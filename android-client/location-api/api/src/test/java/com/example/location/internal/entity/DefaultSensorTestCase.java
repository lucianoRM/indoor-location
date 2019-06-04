package com.example.location.internal.entity;

import com.example.location.api.data.DataTransformer;
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
import java.util.List;

import static org.hamcrest.CoreMatchers.equalTo;
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
    public void sensorGetsObjectsFromFeed() {
        SensorFeed sensorFeed = mock(SensorFeed.class);
        DataTransformer dataTransformer = mock(DataTransformer.class);
        SensorListener sensorListener = mock(SensorListener.class);
        EmitterManager emitterManager = mock(EmitterManager.class);

        final String emitterId1 = "e1";
        final String emitterId2 = "e2";
        final SignalEmitter se1 = mock(SignalEmitter.class);
        final SignalEmitter se2 = mock(SignalEmitter.class);
        when(se1.getId()).thenReturn(emitterId1);
        when(se2.getId()).thenReturn(emitterId2);

        List<RawSensorData> sensedDataList = new ArrayList<>();
        sensedDataList.add(new RawSensorData(emitterId1, 0.0f));
        sensedDataList.add(new RawSensorData(emitterId2, 0.0f));
        when(sensorFeed.getData()).thenReturn(sensedDataList);

        List<SensorData> transformedData = new ArrayList<>();
        transformedData.add(new SensorData(0.0f, 0L));
        transformedData.add(new SensorData(0.0f, 0L));
        when(dataTransformer.transform(any(), eq(sensedDataList.get(0)))).thenReturn(transformedData.get(0));
        when(dataTransformer.transform(any(), eq(sensedDataList.get(1)))).thenReturn(transformedData.get(1));

        when(emitterManager.getSignalEmitter(eq(emitterId1))).thenReturn(of(se1));
        when(emitterManager.getSignalEmitter(eq(emitterId2))).thenReturn(of(se2));

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
