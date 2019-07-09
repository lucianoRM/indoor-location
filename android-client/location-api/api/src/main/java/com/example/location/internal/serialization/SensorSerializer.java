package com.example.location.internal.serialization;

import com.example.location.api.entity.sensor.Sensor;

import java.lang.reflect.Type;

public class SensorSerializer extends InterfaceSerializer<Sensor> {

    @Override
    protected Type getImplementationTypeForDeserialization() {
        return SensorView.class;
    }

}
