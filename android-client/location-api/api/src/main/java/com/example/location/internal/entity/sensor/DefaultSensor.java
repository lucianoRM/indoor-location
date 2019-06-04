package com.example.location.internal.entity.sensor;

import com.example.location.api.data.DataTransformer;
import com.example.location.api.data.RawSensorData;
import com.example.location.api.system.EmitterManager;
import com.example.location.internal.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorFeed;

import java.util.ArrayList;
import java.util.List;

/**
 * Default implementation for a {@link Sensor}
 */

public class DefaultSensor implements Sensor {

    private String id;
    private String name;
    private SensorFeed feed;
    private DataTransformer sensedDataTransformer;
    private SensorListener listener;
    private EmitterManager emitterManager;

    public DefaultSensor(String id,
                         String name,
                         SensorFeed feed,
                         DataTransformer sensedDataTransformer,
                         SensorListener listener,
                         EmitterManager emitterManager) {
        this.id = id;
        this.name = name;
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
                data -> emitterManager.getSignalEmitter(data.getEmitterId())
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

    @Override
    public String getId() {
        return this.id;
    }

    @Override
    public String getName() {
        return this.name;
    }
}
