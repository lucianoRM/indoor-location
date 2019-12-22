package com.example.location.internal.entity.sensor;

import com.example.location.api.entity.sensor.SensingException;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.system.async.AsyncCallback;
import com.example.location.internal.entity.SkeletalIdentifiableObject;

public class SensorView extends SkeletalIdentifiableObject implements Sensor {

    public SensorView(String id, String name) {
        super(id, name);
    }

    @Override
    public void sense() throws SensingException {
        throw new UnsupportedOperationException("SensorView has not ability to sense");
    }
}
