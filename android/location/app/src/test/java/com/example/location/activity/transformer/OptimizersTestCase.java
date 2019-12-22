package com.example.location.activity.transformer;

import com.example.location.api.data.Position;
import com.example.location.api.data.RawSensorData;
import com.example.location.api.data.SensorData;
import com.example.location.api.data.Signal;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.SensorContext;
import com.example.location.impl.ble.ibeacon.transfomers.OptimizationBasedSensorDataTransformer;
import com.example.location.internal.logger.ServerLogger;

import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

import static com.example.location.impl.RadioDataTransformer.MEDIUM_COEFFICIENT_SIGNAL_KEY;
import static com.example.location.impl.RadioDataTransformer.ONE_METER_POWER_SIGNAL_KEY;
import static com.example.location.impl.ble.ibeacon.transfomers.BasePowerOptimizationBasedValueResolver.basePowerOptimizationValueResolver;
import static com.example.location.impl.ble.ibeacon.transfomers.CoeffAndBasePowerOptimizationBasedValueResolver.coeffAndBasePowerValueResolver;
import static com.example.location.impl.ble.ibeacon.transfomers.CoeffOptimizationValueResolver.coeffOptimizationValueResolver;
import static java.util.Optional.of;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class OptimizersTestCase {

    @Test
    public void optimizersResultsMakeSense() {
        ServerLogger serverLogger = mock(ServerLogger.class);

        final String emitterId = "emitter";
        final String emitterAId = "A";
        final String emitterBId = "B";

        final String basePower = "-60.0";
        final String powerMeasuredByA = "-69.0";
        final String powerMeasuredByB = "-72.0";

        final String mediumCoeff = "3.0";

        SignalEmitter seA = mock(SignalEmitter.class);
        SignalEmitter seB = mock(SignalEmitter.class);
        SignalEmitter se = mock(SignalEmitter.class);

        Position positionA = mock(Position.class);
        when(positionA.getX()).thenReturn(0.0f);
        when(positionA.getY()).thenReturn(2.0f);
        when(seA.getPosition()).thenReturn(positionA);

        Position positionB = mock(Position.class);
        when(positionB.getX()).thenReturn(2.0f);
        when(positionB.getY()).thenReturn(0.0f);
        when(seB.getPosition()).thenReturn(positionB);

        Position position = mock(Position.class);
        when(position.getX()).thenReturn(0.0f);
        when(position.getY()).thenReturn(0.0f);
        when(se.getPosition()).thenReturn(position);

        Signal signal = mock(Signal.class);
        when(signal.getAttribute(ONE_METER_POWER_SIGNAL_KEY)).thenReturn(of(basePower));
        when(signal.getAttribute(MEDIUM_COEFFICIENT_SIGNAL_KEY)).thenReturn(of(mediumCoeff));
        when(signal.getAttribute("PWR_AVG_BY_A")).thenReturn(of(powerMeasuredByA));
        when(signal.getAttribute("PWR_AVG_BY_B")).thenReturn(of(powerMeasuredByB));

        when(se.getSignal()).thenReturn(signal);

        RawSensorData rawSensorData = mock(RawSensorData.class);
        when(rawSensorData.getEmitterId()).thenReturn(emitterId);
        when(rawSensorData.getAttribute("SENSED_POWER")).thenReturn(-100);
        when(rawSensorData.getAttribute("TIMESTAMP")).thenReturn(0L);

        SensorContext sensorContext = mock(SensorContext.class);

        Map<String, SignalEmitter> signalEmitters = new HashMap<>();
        signalEmitters.put(emitterId, se);
        signalEmitters.put(emitterAId, seA);
        signalEmitters.put(emitterBId, seB);
        when(sensorContext.getSignalEmitters()).thenReturn(signalEmitters);

        OptimizationBasedSensorDataTransformer coeffTransformer = new OptimizationBasedSensorDataTransformer(coeffOptimizationValueResolver(), "opCoeff", serverLogger);
        OptimizationBasedSensorDataTransformer basePowerTransformer = new OptimizationBasedSensorDataTransformer(basePowerOptimizationValueResolver(), "opBp", serverLogger);
        OptimizationBasedSensorDataTransformer coeffAndPowerTransformer = new OptimizationBasedSensorDataTransformer(coeffAndBasePowerValueResolver(),"opCoeffBp", serverLogger);

        SensorData coeffData = coeffTransformer.transform(rawSensorData, sensorContext);
        SensorData basePowerData = basePowerTransformer.transform(rawSensorData, sensorContext);
        SensorData coeffAndBasePowerData = coeffAndPowerTransformer.transform(rawSensorData, sensorContext);

        System.out.println("COEFF: " + coeffData.getDistance());
        System.out.println("BP: " + basePowerData.getDistance());
        System.out.println("CEFF + BP: " + coeffAndBasePowerData.getDistance());

    }

}
