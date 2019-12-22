package com.example.location.impl.ble.ibeacon.transfomers;


import com.example.location.api.data.Signal;
import com.example.location.api.entity.sensor.SensorContext;
import com.example.location.api.data.RawSensorData;
import com.example.location.api.data.SensorData;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.logger.ServerLogger;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;

import static com.example.location.internal.logger.ServerLogEntry.entry;
import static java.lang.Double.parseDouble;
import static java.lang.StrictMath.sqrt;

/**
 * Computes distances to beacons by using measuring information provided by the server.
 * The result base power is computed by building an optimization problem.
 *
 * Lets call B the beacon from which we want to know the distance.
 * Each other beacon in range from B will update the server with the power it senses from it.
 * Since we know all beacons positions, we can compute the distance to B easily.
 * And we know that:
 *
 *    d = 10 ^ [ (basePower - sensedPower ) / (10 C) ] , C being a medium coefficient.
 *
 * Then, we can run an optimization problem for every beacon in range of B and approximate
 * it's basePower knowing that it should be the same for all beacons in range.
 *
 */
public class OptimizationBasedSensorDataTransformer extends AbstractBleBeaconTransformer {

    private static final String PWR_AVG_PREFIX = "PWR_AVG_BY_";

    private OptimizationBasedValueResolverFactory resolverFactory;

    private OptimizationBasedValueResolver resolver;

    public OptimizationBasedSensorDataTransformer(OptimizationBasedValueResolverFactory resolverFactory,
                                                  String name,
                                                  ServerLogger serverLogger) {
        super(name, serverLogger);
        this.resolverFactory = resolverFactory;
    }

    @Override
    public SensorData transform(RawSensorData rawData, SensorContext context) {

        //TODO: Avoid doing all this if the information in the server did not change.

        resolver = null; //Set this to null to be able to fallback to parents behaviour.

        SignalEmitter signalEmitter = context.getSignalEmitters().get(rawData.getEmitterId());

        Map<String, Double> powerAverages = getAllPowerAverages(signalEmitter.getSignal(), context.getSignalEmitters().keySet());

        List<Double> measuredPowers = new LinkedList<>();
        List<Double> distances = new LinkedList<>();

        powerAverages.forEach(
                (k, v) -> {
                    measuredPowers.add(v);
                    distances.add(getDistance(signalEmitter, context.getSignalEmitters().get(k)));
                }
        );

        if(!measuredPowers.isEmpty()) {
            resolver = resolverFactory.getResolver(distances, measuredPowers, signalEmitter);
            resolver.solve();

            StringBuilder stringBuilder = new StringBuilder();
            stringBuilder.append("optimizing for [");
            powerAverages.forEach((k,v) -> {
                stringBuilder.append("se: ");
                stringBuilder.append(k);
                stringBuilder.append("->");
                stringBuilder.append(v);
                stringBuilder.append(" ");
            });
            stringBuilder.append("]");
            serverLogger.logInServer(entry("TRANSFORMER", stringBuilder.toString()));
        }
        return super.transform(rawData, context);
    }

    @Override
    protected float getBasePower(RawSensorData rawSensorData, SensorContext context) {
        if(resolver != null) {
            return resolver.getBasePower();
        }
        return super.getBasePower(rawSensorData, context);
    }

    @Override
    protected float getMediumCoeff(RawSensorData rawSensorData, SensorContext context) {
        if(resolver != null) {
            return resolver.getMediumCoeff();
        }
        return super.getMediumCoeff(rawSensorData, context);
    }

    private Map<String, Double> getAllPowerAverages(Signal signal, Set<String> signalEmittersIds) {
        Map<String, Double> allPowerAverages = new HashMap<>();
        signalEmittersIds.forEach(
                id -> {
                    final String powerKey = buildSignalPowerKey(id);
                    signal.getAttribute(powerKey).ifPresent(v -> allPowerAverages.put(id, parseDouble(v)));
                }
        );
        return allPowerAverages;
    }

    private double getDistance(SignalEmitter emitterUnderTest, SignalEmitter other) {
        final double xDiff = emitterUnderTest.getPosition().getX() - other.getPosition().getX();
        final double yDiff = emitterUnderTest.getPosition().getY() - other.getPosition().getY();
        return sqrt((xDiff * xDiff) + (yDiff * yDiff));
    }

    private String buildSignalPowerKey(String measuringSeId) {
        return PWR_AVG_PREFIX + measuringSeId;
    }
}
