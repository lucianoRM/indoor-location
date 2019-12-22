package com.example.location.api.utils;

import java.util.ArrayList;
import java.util.List;

import static com.google.common.math.Stats.meanOf;
import static java.util.Collections.sort;

public class SensingUtils {

    /**
     * Compute the best value according to the list of measurements.
     * Remove bottom 20% and upper 10%, then average.
     */
    public static <T extends Number & Comparable<? super T>> double bestValueFrom(List<T> measurements) {
        if(measurements.isEmpty()) {
            return 0;
        }
        List<T> localMeasurements = new ArrayList<>(measurements);
        int size = localMeasurements.size();
        sort(localMeasurements);
        if(size >= 3) {
            int lowerValuesPosition = (int)(size * 0.2);
            int upperValuePosition = (int)(size * 0.9);
            for(int i = 0; i<lowerValuesPosition; i++) {
                localMeasurements.remove(0);
            }
            for(int i = upperValuePosition; i<size; i++) {
                localMeasurements.remove(localMeasurements.size() - 1);
            }
        }
        return meanOf(localMeasurements);
    }

}
