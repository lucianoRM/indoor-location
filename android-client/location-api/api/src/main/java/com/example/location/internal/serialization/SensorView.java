package com.example.location.internal.serialization;

import com.example.location.api.data.Position;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.internal.entity.SkeletalIdentifiableObject;

public class SensorView extends SkeletalIdentifiableObject implements Sensor {

    public SensorView(String id, String name, Position position) {
        super(id, name, position);
    }

    @Override
    public void sense() {
        throw new UnsupportedOperationException("SensorView has not ability to sense");
    }
}
