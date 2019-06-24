package com.example.location.impl.wifi;

import android.net.wifi.ScanResult;

import com.example.location.api.data.DataTransformer;
import com.example.location.api.data.RawSensorData;
import com.example.location.api.data.SensorData;
import com.example.location.api.entity.emitter.SignalEmitter;

import java.util.function.Supplier;

import static com.example.location.impl.wifi.WiFiSensorFeed.SCAN_RESULT;
import static java.lang.Integer.parseInt;
import static java.lang.Math.log10;

public class WifiTransformer implements DataTransformer {

    private static final String MAX_SIGNAL_POWER = "MAX_POWER";

    @Override
    public SensorData transform(SignalEmitter signalEmitter, RawSensorData rawData) {
        try {
            int maxPower = signalEmitter.getSignal().getAttribute(MAX_SIGNAL_POWER).map(Integer::parseInt).orElseThrow(() -> new RuntimeException("Signal does not have max power"));
        } catch (Throwable e) {
            throw new RuntimeException(e);
        }
        ScanResult scanResult = rawData.getAttribute(SCAN_RESULT);
        return new SensorData(0,0);
    }

    private float computeDistance(int maxPower, int frequency, int sensedPower) {
        return 0.0f;
    }
}
