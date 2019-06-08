package com.example.location.functional;

import com.example.location.api.data.DataTransformer;
import com.example.location.api.data.RawSensorData;
import com.example.location.api.data.SensorData;
import com.example.location.api.entity.emitter.SignalEmitter;

public class TestDataTransformer implements DataTransformer {

    private static final SensorData SENSOR_DATA = new SensorData(10, 0);

    @Override
    public SensorData transform(SignalEmitter signalEmitter, RawSensorData rawData) {
        return SENSOR_DATA;
    }
}
