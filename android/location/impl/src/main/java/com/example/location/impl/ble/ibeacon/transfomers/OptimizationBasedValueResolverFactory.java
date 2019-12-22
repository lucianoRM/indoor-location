package com.example.location.impl.ble.ibeacon.transfomers;

import com.example.location.api.entity.emitter.SignalEmitter;

import java.util.List;

public interface OptimizationBasedValueResolverFactory {

    OptimizationBasedValueResolver getResolver(List<Double> distances, List<Double> measuredPowers, SignalEmitter signalEmitter);

}
