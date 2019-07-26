package com.example.location.impl.wifi;

import static java.lang.Math.pow;

/**
 * Utils class for computing operations related to signals
 */
public class SignalUtils {

    private static final float MEDIUM_COEFFICIENT = 2.2f;

    /**
     * TODO:ADD JAVADOC
     */
    public static float computeDistance(float oneMeterPower, int sensedPower) {
        float exp = (oneMeterPower - sensedPower)/(10 * MEDIUM_COEFFICIENT);
        return (float)pow(10, exp);
    }
}
