package com.example.location.internal.entity.sensor;


import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.SensorContext;
import com.example.location.api.entity.sensor.SensorDataTransformer;
import com.example.location.api.data.RawSensorData;
import com.example.location.api.entity.sensor.SensingException;
import com.example.location.api.system.EmitterManager;
import com.example.location.api.system.EmitterManagerException;
import com.example.location.internal.ThrowingConsumer;
import com.example.location.internal.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorFeed;
import com.example.location.internal.entity.SkeletalIdentifiableObject;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;


/**
 * Default implementation for a {@link Sensor}
 */

public class DefaultSensor extends SkeletalIdentifiableObject implements Sensor {

    private transient SensorFeed feed;
    private transient SensorDataTransformer sensedDataTransformer;
    private transient SensorListener sensorListener;
    private transient EmitterManager emitterManager;

    public DefaultSensor(String id,
                         String name,
                         SensorFeed feed,
                         SensorDataTransformer sensedDataTransformer,
                         SensorListener sensorListener,
                         EmitterManager emitterManager) {
        super(id, name);
        this.feed = feed;
        this.sensedDataTransformer = sensedDataTransformer;
        this.sensorListener = sensorListener;
        this.emitterManager = emitterManager;
    }

    @Override
    public void sense() throws SensingException {
        List<RawSensorData> sensedObjectsData = feed.getData();
        List<SensedObject> transformedObjects = new ArrayList<>();
        try {
            Map<String, SignalEmitter> serverSignalEmitters = emitterManager.getSignalEmitters();
            SensorContext context = new DefaultSensorContext(serverSignalEmitters);
            sensedObjectsData.forEach(
                    (ThrowingConsumer<RawSensorData, EmitterManagerException>) data -> {
                        if (serverSignalEmitters.containsKey(data.getEmitterId())) {
                            transformedObjects.add(
                                    new SensedObject(
                                            data.getEmitterId(),
                                            sensedDataTransformer.transform(data, context)
                                    )
                            );
                        }
                    }
            );
            sensorListener.onSensorUpdate(this, transformedObjects);
        } catch (Exception e) {
            throw new SensingException("Error while sensing", e);
        }
    }

}
