package com.example.location.impl.ble.ibeacon.transfomers;

public interface OptimizationBasedValueResolver {

    /**
     * Run the optimizer
     */
    void solve();

    float getMediumCoeff();

    float getBasePower();

}
