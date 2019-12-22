package com.example.location.impl.ble.ibeacon;

import com.example.location.api.data.RawSensorData;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.SensorContext;
import com.example.location.impl.RadioDataTransformer;

import java.util.ArrayList;
import java.util.List;

import static com.example.location.impl.ble.ibeacon.IBeaconSensorFeed.SENSED_POWER;
import static com.example.location.impl.ble.ibeacon.IBeaconSensorFeed.TIMESTAMP;
import static com.google.common.math.Stats.meanOf;
import static java.lang.Float.parseFloat;

public class IBeaconDataTransformer extends RadioDataTransformer {

    private static final String COEF_KEY_PREFIX = "MEDIUM_COEF_BY_";

    @Override
    protected int getMeasuredPower(RawSensorData rawSensorData) {
        return rawSensorData.getAttribute(SENSED_POWER);
    }

    /**
     * Check all sensed beacons and find their calibrated coefficients regarding the sensed signal emitter.
     * Return the average of that
     */
    @Override
    protected float getMediumCoef(RawSensorData rawSensorData, SensorContext context) {
        List<Float> calibratedCoefficients = new ArrayList<>();
        SignalEmitter signalEmitter = context.getSignalEmitters().get(rawSensorData.getEmitterId());
        context.getSignalEmitters().keySet().forEach(
                b -> signalEmitter.getSignal().getAttribute(buildMediumCoefKey(b)).ifPresent(
                        v -> {
                            float f = parseFloat(v);
                            if(f > 0) {
                                calibratedCoefficients.add(f);
                            }
                        }
                )
        );
        if(!calibratedCoefficients.isEmpty()) {
            return (float)meanOf(calibratedCoefficients);
        }
        return super.getMediumCoef(rawSensorData, context);
    }

    private String buildMediumCoefKey(String id) {
        return COEF_KEY_PREFIX + id;
    }

    @Override
    protected long getTimestamp(RawSensorData rawSensorData) {
        return rawSensorData.getAttribute(TIMESTAMP);
    }
}
