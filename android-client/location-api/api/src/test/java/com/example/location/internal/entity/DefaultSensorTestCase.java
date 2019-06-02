package com.example.location.internal.entity;

import com.example.location.api.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorFeed;
import com.example.location.internal.entity.sensor.DefaultSensor;
import com.example.location.internal.entity.sensor.SensorListener;
import org.junit.Test;

import java.util.ArrayList;
import java.util.List;

import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

public class DefaultSensorTestCase {

    @Test
    public void sensorGetsObjectsFromFeed() {
        SensorFeed sensorFeed = mock(SensorFeed.class);
        SensorListener sensorListener = mock(SensorListener.class);

        List<SensedObject> sensedObjectList = new ArrayList<>();
        sensedObjectList.add(new SensedObject("so1", null));
        sensedObjectList.add(new SensedObject("so2", null));

        when(sensorFeed.getSensedObjects()).thenReturn(sensedObjectList);
        Sensor sensor = new DefaultSensor("id", "name", sensorFeed, sensorListener);
        sensor.sense();
        verify(sensorListener).onSensorUpdate(eq(sensor), eq(sensedObjectList));
    }

}
