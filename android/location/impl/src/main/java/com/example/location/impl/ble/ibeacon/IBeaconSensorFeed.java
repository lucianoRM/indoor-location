package com.example.location.impl.ble.ibeacon;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.bluetooth.le.ScanSettings;
import android.util.Pair;

import com.example.location.api.data.RawSensorData;
import com.example.location.api.entity.sensor.SensorFeed;
import com.example.location.internal.logger.ServerLogEntry;
import com.example.location.internal.logger.ServerLogger;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import mobi.inthepocket.android.beacons.ibeaconscanner.Beacon;

import static android.bluetooth.le.ScanSettings.SCAN_MODE_LOW_LATENCY;
import static com.example.location.api.utils.SensingUtils.bestValueFrom;
import static com.example.location.internal.logger.ServerLogEntry.entry;
import static com.google.common.primitives.Ints.asList;
import static java.lang.System.nanoTime;
import static java.util.concurrent.TimeUnit.MILLISECONDS;
import static java.util.stream.Collectors.toSet;
import static mobi.inthepocket.android.beacons.ibeaconscanner.utils.BeaconUtils.createBeaconFromScanRecord;
import static mobi.inthepocket.android.beacons.ibeaconscanner.utils.BeaconUtils.isBeaconPattern;

public class IBeaconSensorFeed implements SensorFeed {

    static final String SENSED_POWER = "SENSED_POWER";
    static final String TIMESTAMP = "TIMESTAMP";

    //Max time a BLE beacon will be without advertising itself
    private static final long MAX_ADVERTISING_TIME = MILLISECONDS.toNanos(20240);

    private final Object lock = new Object();
    private Map<String, SensorDataInformation> sensedDataInformation = new HashMap<>();
    private Map<String, RawSensorData> sensedData = new HashMap<>();
    private ScanCallback scanCallback;
    private BluetoothLeScanner bleScanner;
    private ServerLogger logger;

    public IBeaconSensorFeed(ServerLogger logger) {
        this.logger = logger;
        this.bleScanner = BluetoothAdapter.getDefaultAdapter().getBluetoothLeScanner();
        this.scanCallback = new ScanCallback() {
            @Override
            public void onScanResult(int callbackType, ScanResult result) {
                Pair<Boolean, Integer> isBeaconPattern = isBeaconPattern(result);
                if(!isBeaconPattern.first) {
                    return;
                }
                final Beacon beacon = createBeaconFromScanRecord(result.getScanRecord().getBytes(), isBeaconPattern.second);
                //TODO: Remove this. We should use the UUID directly.
                String id = Long.toString(beacon.getUUID().getLeastSignificantBits());
                final long timestamp = nanoTime();
                synchronized (lock) {
                    SensorDataInformation dataInfo = sensedDataInformation.compute(id, (k,v) -> {
                        if(v == null) {
                            return new SensorDataInformation(timestamp);
                        }
                        v.setLastMeasuredTimestamp(timestamp);
                        return v;
                    });
                    int power = dataInfo.getPowerAverage(result.getRssi());
                    RawSensorData rawSensorData = new RawSensorData(id);
                    rawSensorData.addAttribute(SENSED_POWER, power);
                    rawSensorData.addAttribute(TIMESTAMP, timestamp);
                    sensedData.put(id, rawSensorData);
                }
            }
        };
    }

    public void start() {
        bleScanner.startScan(null,
                new ScanSettings.Builder().setScanMode(SCAN_MODE_LOW_LATENCY).build(),
                scanCallback);
    }

    public void stop() {
        bleScanner.stopScan(scanCallback);
    }

    @Override
    public List<RawSensorData> getData() {
        synchronized (lock) {
            long timestamp = nanoTime();
            Set<String> idsToRemove = sensedDataInformation.entrySet().stream().filter((e) -> (timestamp - e.getValue().getLastMeasuredTimestamp()) > MAX_ADVERTISING_TIME).map(Map.Entry::getKey).collect(toSet());
            sensedDataInformation.keySet().removeAll(idsToRemove);
            sensedData.keySet().removeAll(idsToRemove);

            StringBuilder sb = new StringBuilder();
            sb.append("FEED: {").append("\n");

            for(Map.Entry<String, SensorDataInformation> info : sensedDataInformation.entrySet()) {
                sb.append(info.getKey()).append(": [");
                for(Integer value : info.getValue().lastNElements) {
                    sb.append(value).append(", ");
                }
                sb.append("]\n");
            }

            logger.logInServer(entry("FEED", sb.toString()));

            return new ArrayList<>(sensedData.values());
        }
    }

    private static class SensorDataInformation {

        private static final int TOTAL_ELEMENTS = 30;
        private int[] lastNElements;
        private int position;

        private long lastMeasuredTimestamp;

        SensorDataInformation(long timestamp) {
            this.position = 0;
            this.lastMeasuredTimestamp = timestamp;
            this.lastNElements = new int[TOTAL_ELEMENTS];
            for(int i = 0; i < TOTAL_ELEMENTS; i++) {
                this.lastNElements[i] = 0;
            }
        }

        public long getLastMeasuredTimestamp() {
            return this.lastMeasuredTimestamp;
        }

        public void setLastMeasuredTimestamp(long timestamp) {
            this.lastMeasuredTimestamp = timestamp;
        }

        public int getPowerAverage(int newMeasurement) {
            this.lastNElements[position] = newMeasurement;
            position = (position + 1)%TOTAL_ELEMENTS;
            return (int)bestValueFrom(asList(lastNElements));
        }

        public int getNMeasurements() {
            return (position < TOTAL_ELEMENTS) && (lastNElements[TOTAL_ELEMENTS-1] == 0) ? position : TOTAL_ELEMENTS;
        }

    }
}
