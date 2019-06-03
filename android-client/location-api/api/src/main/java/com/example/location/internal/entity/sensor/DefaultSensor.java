package com.example.location.internal.entity.sensor;

import com.example.location.api.data.DataTransformer;
import com.example.location.api.data.RawSensorData;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.data.SensedObject;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorFeed;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static java.util.stream.Collectors.toList;

public class DefaultSensor implements Sensor {

    private String id;
    private String name;
    private SensorFeed feed;
    private DataTransformer sensedDataTransformer;
    private SensorListener listener;

    public DefaultSensor(String id,
                         String name,
                         SensorFeed feed,
                         DataTransformer sensedDataTransformer,
                         SensorListener listener) {
        this.id = id;
        this.name = name;
        this.feed = feed;
        this.sensedDataTransformer = sensedDataTransformer;
        this.listener = listener;
    }

    @Override
    public void sense() {
        List<RawSensorData> sensedObjectsData = feed.getData();
        final Map<String,SignalEmitter> validEmitters = new HashMap<>();
        List<SensedObject> transformedObjects = sensedObjectsData
                .stream()
                .filter((a) -> true)//sensorData -> validEmitters.containsKey(sensorData.getEmitterId()))
                .map(sensorData -> {
                    SignalEmitter emitter = validEmitters.get(sensorData.getEmitterId());
                    return new SensedObject(
                            emitter.getId(),
                            sensedDataTransformer.transform(emitter, sensorData)
                    );
                })
                .collect(toList());
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
