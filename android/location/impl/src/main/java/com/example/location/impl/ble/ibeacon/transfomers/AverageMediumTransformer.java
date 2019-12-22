package com.example.location.impl.ble.ibeacon.transfomers;

import com.example.location.api.entity.sensor.SensorContext;
import com.example.location.api.data.RawSensorData;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.logger.ServerLogger;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import static com.google.common.math.Stats.meanOf;
import static java.lang.Float.parseFloat;

public class AverageMediumTransformer extends AbstractBleBeaconTransformer {

    private static final String COEF_KEY_PREFIX = "MEDIUM_COEF_BY_";

    public AverageMediumTransformer(ServerLogger serverLogger) {
        super("AVG", serverLogger);
    }

    protected float getMediumCoeff(RawSensorData rawSensorData, SensorContext context) {
        SignalEmitter signalEmitter = context.getSignalEmitters().get(rawSensorData.getEmitterId());
        Set<String> allSensedBeacons = context.getSignalEmitters().keySet();
        List<Float> calibratedCoefficients = new ArrayList<>();
        allSensedBeacons.forEach(
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
        return super.getMediumCoeff(rawSensorData, context);
    }

    private String buildMediumCoefKey(String id) {
        return COEF_KEY_PREFIX + id;
    }

}
