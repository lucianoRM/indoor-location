package com.example.location.impl.wifi;

import android.net.wifi.ScanResult;

import com.example.location.api.data.RawSensorData;
import com.example.location.impl.RadioDataTransformer;

import static com.example.location.impl.wifi.WiFiSensorFeed.SCAN_RESULT;

public class WifiTransformer extends RadioDataTransformer {

    @Override
    protected int getMeasuredPower(RawSensorData rawSensorData) {
        ScanResult scanResult = rawSensorData.getAttribute(SCAN_RESULT);
        return scanResult.level;
    }

    @Override
    protected long getTimestamp(RawSensorData rawSensorData) {
        ScanResult scanResult = rawSensorData.getAttribute(SCAN_RESULT);
        return scanResult.timestamp;
    }
}
