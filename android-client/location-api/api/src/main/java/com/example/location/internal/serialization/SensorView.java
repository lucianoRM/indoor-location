package com.example.location.internal.serialization;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.internal.entity.SkeletalIdentifiableObject;

public class SensorView extends SkeletalIdentifiableObject implements Sensor {

    public SensorView(String id, String name) {
        super(id, name);
    }

    @Override
    public void sense() {
        throw new UnsupportedOperationException("SensorView has not ability to sense");
    }
}
