package com.example.location.impl.wifi;

import android.net.wifi.ScanResult;

import com.example.location.api.data.DataTransformer;
import com.example.location.api.data.RawSensorData;
import com.example.location.api.data.SensorData;
import com.example.location.api.entity.emitter.SignalEmitter;

import static com.example.location.impl.wifi.SignalUtils.computeDistance;
import static com.example.location.impl.wifi.WiFiSensorFeed.SCAN_RESULT;

public class WifiTransformer implements DataTransformer {

    private static final float DEFAULT_ONE_METER_POWER = -23.0f;
    private static final String ONE_METER_SIGNAL_POWER = "MAX_POWER";

    @Override
    public SensorData transform(SignalEmitter signalEmitter, RawSensorData rawData) {
        float powerAt1Meter = signalEmitter
                .getSignal()
                .getAttribute(ONE_METER_SIGNAL_POWER)
                .map(Float::parseFloat)
                .orElse(DEFAULT_ONE_METER_POWER);
        ScanResult scanResult = rawData.getAttribute(SCAN_RESULT);
        return new SensorData(computeDistance(powerAt1Meter, scanResult.level),scanResult.timestamp);
    }

}
