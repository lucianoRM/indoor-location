package com.example.location.internal.entity.sensor;

import com.example.location.api.data.DataTransformer;
import com.example.location.api.data.Position;
import com.example.location.api.data.RawSensorData;
import com.example.location.api.system.EmitterManager;
import com.example.location.api.system.EmitterManagerException;
import com.example.location.internal.ThrowingConsumer;
import com.example.location.internal.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorFeed;
import com.example.location.internal.entity.SkeletalIdentifiableObject;

import java.util.ArrayList;
import java.util.List;

/**
 * Default implementation for a {@link Sensor}
 */

public class DefaultSensor extends SkeletalIdentifiableObject implements Sensor {

    private transient SensorFeed feed;
    private transient DataTransformer sensedDataTransformer;
    private transient SensorListener listener;
    private transient EmitterManager emitterManager;

    public DefaultSensor(String id,
                         String name,
                         SensorFeed feed,
                         DataTransformer sensedDataTransformer,
                         SensorListener listener,
                         EmitterManager emitterManager) {
        super(id, name, new Position(0, 0));
        this.feed = feed;
        this.sensedDataTransformer = sensedDataTransformer;
        this.listener = listener;
        this.emitterManager = emitterManager;
    }

    @Override
    public void sense() {
        List<RawSensorData> sensedObjectsData = feed.getData();
        List<SensedObject> transformedObjects = new ArrayList<>();

        sensedObjectsData.forEach(
                (ThrowingConsumer<RawSensorData, EmitterManagerException>) data -> emitterManager.getSignalEmitter(data.getEmitterId())
                        .ifPresent(
                                emitter -> transformedObjects.add(
                                        new SensedObject(
                                                emitter.getId(),
                                                sensedDataTransformer.transform(emitter, data)
                                        )
                                )
                        )
        );

        listener.onSensorUpdate(this, transformedObjects);
    }
}
