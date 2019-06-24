package com.example.location.impl.wifi;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;

import com.example.location.api.data.RawSensorData;
import com.example.location.api.entity.sensor.SensorFeed;

import java.util.ArrayList;
import java.util.List;

import static android.content.Context.WIFI_SERVICE;
import static android.net.wifi.WifiManager.EXTRA_RESULTS_UPDATED;
import static android.net.wifi.WifiManager.SCAN_RESULTS_AVAILABLE_ACTION;

public class WiFiSensorFeed implements SensorFeed {

    static final String SCAN_RESULT = "SCAN_RESULT";

    private WifiManager wifiManager;
    private List<RawSensorData> lastScannedElements;

    private final Object updateLock = new Object();

    public WiFiSensorFeed(Context context) {
        this.wifiManager = (WifiManager) context.getSystemService(WIFI_SERVICE);
        this.lastScannedElements = new ArrayList<>();

        BroadcastReceiver wifiScanReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                boolean success = intent.getBooleanExtra(EXTRA_RESULTS_UPDATED, false);
                if (success) {
                    scanSuccess();
                }
            }
        };

        IntentFilter intentFilter = new IntentFilter();
        intentFilter.addAction(SCAN_RESULTS_AVAILABLE_ACTION);
        context.registerReceiver(wifiScanReceiver, intentFilter);
    }

    private void scanSuccess() {
        synchronized (updateLock) {
            lastScannedElements = new ArrayList<>();
            List<ScanResult> results = wifiManager.getScanResults();
            for (ScanResult scanResult : results) {
                RawSensorData sensorData = new RawSensorData(scanResult.SSID);
                sensorData.addAttribute(SCAN_RESULT, scanResult);
                lastScannedElements.add(sensorData);
            }
        }
    }

    @Override
    public List<RawSensorData> getData() {
        synchronized (updateLock) {
            return this.lastScannedElements;
        }
    }
}
