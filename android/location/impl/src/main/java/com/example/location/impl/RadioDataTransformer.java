package com.example.location.impl;

import com.example.location.api.entity.sensor.SensorContext;
import com.example.location.api.entity.sensor.SensorDataTransformer;
import com.example.location.api.data.RawSensorData;
import com.example.location.api.data.SensorData;
import com.example.location.api.entity.emitter.SignalEmitter;

import static com.example.location.impl.SignalUtils.computeDistance;

public abstract class RadioDataTransformer implements SensorDataTransformer {

    public static final String ONE_METER_POWER_SIGNAL_KEY = "MAX_POWER";
    public static final String MEDIUM_COEFFICIENT_SIGNAL_KEY = "MEDIUM_COEF";

    protected static final float DEFAULT_ONE_METER_POWER = -60.0f;
    protected static final float DEFAULT_MEDIUM_COEF = 4.0f;

    @Override
    public SensorData transform(RawSensorData rawData, SensorContext sensorContext) {
        SignalEmitter signalEmitter = sensorContext.getSignalEmitters().get(rawData.getEmitterId());
        float powerAt1Meter = getPowerAtOneMeter(signalEmitter);
        float mediumCoef = getMediumCoef(rawData, sensorContext);
        int measuredPower = getMeasuredPower(rawData);
        long timestamp = getTimestamp(rawData);
        float distance = computeDistance(measuredPower, powerAt1Meter, mediumCoef);
        return new SensorData(distance, timestamp);
    }

    private float getPowerAtOneMeter(SignalEmitter signalEmitter) {
        return signalEmitter
                .getSignal()
                .getAttribute(ONE_METER_POWER_SIGNAL_KEY)
                .map(Float::parseFloat)
                .orElse(DEFAULT_ONE_METER_POWER);
    }

    protected float getMediumCoef(RawSensorData rawSensorData,
                                  SensorContext context) {
        return context
                .getSignalEmitters()
                .get(rawSensorData.getEmitterId())
                .getSignal()
                .getAttribute(MEDIUM_COEFFICIENT_SIGNAL_KEY)
                .map(Float::parseFloat)
                .orElse(DEFAULT_MEDIUM_COEF);
    }

    protected abstract int getMeasuredPower(RawSensorData rawSensorData);

    protected abstract long getTimestamp(RawSensorData rawSensorData);
}
