package com.example.location.impl.ble.ibeacon.transfomers;


import com.example.location.api.data.RawSensorData;
import com.example.location.api.data.SensorData;
import com.example.location.api.entity.sensor.SensorContext;
import com.example.location.api.entity.sensor.SensorDataTransformer;
import com.example.location.internal.async.DefaultAsyncTask;
import com.example.location.internal.logger.ServerLogger;

import static com.example.location.impl.RadioDataTransformer.MEDIUM_COEFFICIENT_SIGNAL_KEY;
import static com.example.location.impl.RadioDataTransformer.ONE_METER_POWER_SIGNAL_KEY;
import static com.example.location.impl.SignalUtils.computeDistance;
import static com.example.location.internal.logger.ServerLogEntry.entry;
import static java.lang.String.format;

public abstract class AbstractBleBeaconTransformer implements SensorDataTransformer {

    private static final String SENSED_POWER = "SENSED_POWER";
    private static final String TIMESTAMP = "TIMESTAMP";
    private static final String LOG_TAG = "LOG";

    private static final float DEFAULT_BASE_POWER = -63.0f;
    private static final float DEFAULT_COEFF = 2.4f;


    protected ServerLogger serverLogger;

    private String name;

    protected AbstractBleBeaconTransformer(String name, ServerLogger serverLogger) {
        this.name = name;
        this.serverLogger = serverLogger;
    }

    @Override
    public SensorData transform(RawSensorData rawData, SensorContext context) {
        float powerAt1Meter = getBasePower(rawData, context);
        float mediumCoef = getMediumCoeff(rawData, context);
        int measuredPower = getMeasuredPower(rawData);
        long timestamp = getTimestamp(rawData);
        float distance = computeDistance(measuredPower, powerAt1Meter, mediumCoef);
        serverLogger.logInServer(entry(
                LOG_TAG,
                format("%s computed distance to SE: %s with values [Tx: %f, C: %f, Rx: %d] is %f",
                        this.name,
                        rawData.getEmitterId(),
                        powerAt1Meter,
                        mediumCoef,
                        measuredPower,
                        distance)
        ));
        return new SensorData(distance, timestamp);
    }

    protected int getMeasuredPower(RawSensorData rawSensorData) {
        return rawSensorData.getAttribute(SENSED_POWER);
    }

    protected long getTimestamp(RawSensorData rawSensorData) {
        return rawSensorData.getAttribute(TIMESTAMP);
    }

    protected float getBasePower(RawSensorData rawSensorData, SensorContext context) {
        return context
                .getSignalEmitters()
                .get(rawSensorData.getEmitterId())
                .getSignal()
                .getAttribute(ONE_METER_POWER_SIGNAL_KEY)
                .map(Float::parseFloat)
                .orElse(DEFAULT_BASE_POWER);
    }

    protected float getMediumCoeff(RawSensorData rawSensorData, SensorContext context) {
        return context
                .getSignalEmitters()
                .get(rawSensorData.getEmitterId())
                .getSignal()
                .getAttribute(MEDIUM_COEFFICIENT_SIGNAL_KEY)
                .map(Float::parseFloat)
                .orElse(DEFAULT_COEFF);
    }


}
