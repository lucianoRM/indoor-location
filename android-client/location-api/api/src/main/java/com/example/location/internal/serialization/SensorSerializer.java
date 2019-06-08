package com.example.location.internal.serialization;

import com.example.location.api.entity.sensor.Sensor;
import com.example.location.internal.entity.sensor.DefaultSensor;

import java.lang.reflect.Type;

public class SensorSerializer extends TypedObjectSerializer<Sensor> {

    @Override
    protected Type getImplementationTypeForDeserialization(String type) {
        return SensorView.class;
    }

    @Override
    protected String getTypeForSerialization(Sensor object) {
        return "USER";
    }
}
