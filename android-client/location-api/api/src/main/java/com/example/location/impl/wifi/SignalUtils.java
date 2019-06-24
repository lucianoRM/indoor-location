package com.example.location.impl.wifi;

import static java.lang.Math.pow;

/**
 * Utils class for computing operations related to signals
 */
public class SignalUtils {

    private static final float K = -27.55f;

    /**
     * The distance is computed using a formula derived from the Free Space Path Loss.
     * (The power lost by a signal as a function of the distance)
     * FSPL(simplified) = SourcePower - ReceiverPower
     * FSPL = 20 log(distance) + 20 log(frequency) + K
     *
     * so:
     *
     * distance = 1/{frequency * [10^(K/20 + ReceiverPower/20 - SourcePower/20)]}
     *
     * We should use the SourcePower in the computation but some testing showed that the masurements
     * were much more accurate considering it 0.
     *
     * @param measuredLevel signal power measured, in dBm
     * @param frequency signal frequency, in MHz.
     */
    public static double computeDistance(int measuredLevel, int frequency) {
        double exponent = (measuredLevel + K)/20f;
        double div = frequency * pow(10, exponent);
        return 1/div;
    }

}
