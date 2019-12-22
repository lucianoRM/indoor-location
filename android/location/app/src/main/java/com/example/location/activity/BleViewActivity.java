package com.example.location.activity;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.bluetooth.le.ScanSettings;
import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Pair;
import android.view.View;
import android.widget.Button;

import com.example.location.R;
import com.example.location.adapter.BleSignalAdapter;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import mobi.inthepocket.android.beacons.ibeaconscanner.Beacon;

import static android.bluetooth.le.ScanSettings.SCAN_MODE_LOW_LATENCY;
import static android.graphics.Color.GREEN;
import static android.graphics.Color.RED;
import static com.example.location.Utils.showError;
import static java.lang.String.format;
import static mobi.inthepocket.android.beacons.ibeaconscanner.utils.BeaconUtils.createBeaconFromScanRecord;
import static mobi.inthepocket.android.beacons.ibeaconscanner.utils.BeaconUtils.isBeaconPattern;

public class BleViewActivity extends AppCompatActivity {

    private RecyclerView bluetoothRecyclerView;
    private BluetoothAdapter bluetoothAdapter;
    private Map<String, BleDevice> bleDevices = new HashMap<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bluetooth_view);
        this.bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

        RecyclerView recyclerView = findViewById(R.id.bleDevicesRecyclerView);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(new BleSignalAdapter(new ArrayList<>(bleDevices.values())));
        this.bluetoothRecyclerView = recyclerView;

    }

    private void addBLEDevice(BleDevice device) {
        bleDevices.put(device.getId(), device);
        bluetoothRecyclerView.setAdapter(new BleSignalAdapter(new ArrayList<>(bleDevices.values())));
    }

    public void scanBleDevices(View view) {
        Button resetButton = view.findViewById(R.id.bleResetButton);
        resetButton.setBackgroundColor(Color.GRAY);

        bluetoothAdapter.getBluetoothLeScanner().startScan(null,
                new ScanSettings.Builder().setScanMode(SCAN_MODE_LOW_LATENCY).build(),
                new ScanCallback() {

            @Override
            public void onScanFailed(int errorCode) {
                scanFailure(errorCode);
            }

            @Override
            public void onScanResult(int callbackType, ScanResult result) {
                String name = result.getDevice().getName();
                if(name == null || name.isEmpty()) {
                    name = result.getDevice().getAddress();
                }
                Pair<Boolean, Integer> isBeaconPattern = isBeaconPattern(result);
                if(isBeaconPattern.first) {
                    final Beacon beacon = createBeaconFromScanRecord(result.getScanRecord().getBytes(), isBeaconPattern.second);
                    name = format("%d (iBeacon)", beacon.getUUID().getLeastSignificantBits());
                }
                addBLEDevice(new BleDevice(name, result.getRssi()));
            }
        });
        scanSuccess();
    }


    private void scanSuccess() {
        this.bleDevices = new HashMap<>();
        findViewById(R.id.bleResetButton).setBackgroundColor(GREEN);
    }

    private void scanFailure(int errorCode) {
        showError(format("Error scanning BLE: %d", errorCode), BleViewActivity.this);
        findViewById(R.id.bleResetButton).setBackgroundColor(RED);
    }

    public static class BleDevice {

        private String id;
        private int power;

        public BleDevice(String id, int power) {
            this.id = id;
            this.power = power;
        }

        public String getId() {
            return id;
        }

        public int getPower() {
            return power;
        }
    }
}
