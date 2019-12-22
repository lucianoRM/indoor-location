package com.example.location.impl;

import static java.lang.Math.pow;

/**
 * Utils class for computing operations related to signals
 */
public class SignalUtils {

    /**
     * TODO:ADD JAVADOC
     */
    public static float computeDistance(int sensedPower, float oneMeterPower, float mediumCoefficient) {
        float exp = (oneMeterPower - sensedPower)/(10 * mediumCoefficient);
        float result = (float)pow(10, exp);
        if(result < 0) {
            return 0;
        }
        return result;
    }
}
