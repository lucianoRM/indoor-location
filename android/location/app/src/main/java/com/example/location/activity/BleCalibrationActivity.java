package com.example.location.activity;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Pair;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.example.location.R;
import com.example.location.adapter.SignalEmittersAdapter;
import com.example.location.task.AsyncTaskException;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import mobi.inthepocket.android.beacons.ibeaconscanner.Beacon;
import okhttp3.Response;

import static com.example.location.api.system.async.AsyncCallback.newCallback;
import static com.example.location.api.system.async.AsyncUtils.executeAsync;
import static com.example.location.Utils.showError;
import static com.example.location.api.utils.SensingUtils.bestValueFrom;
import static com.example.location.task.HttpUtils.updateSignalEmitter;
import static com.google.common.math.Stats.meanOf;
import static java.lang.String.format;
import static mobi.inthepocket.android.beacons.ibeaconscanner.utils.BeaconUtils.createBeaconFromScanRecord;
import static mobi.inthepocket.android.beacons.ibeaconscanner.utils.BeaconUtils.isBeaconPattern;


public class BleCalibrationActivity extends ConnectedActivity {

    private static final int SAMPLE_SIZE = 100;

    private Map<String, List<Integer>> signalEmitters;
    private SignalEmittersAdapter signalEmittersAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ble_calibration);

        this.signalEmittersAdapter = new SignalEmittersAdapter();

        RecyclerView recyclerView = findViewById(R.id.availableActivitiesRecyclerView);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(signalEmittersAdapter);
    }


    public void calibrateSignalEmitter(View signalEmitterCard) {
        TextView emitterIdView = signalEmitterCard.findViewById(R.id.signalEmitterIdCardTextView);
        final String emitterId = emitterIdView.getText().toString();
        BluetoothLeScanner scanner = BluetoothAdapter.getDefaultAdapter().getBluetoothLeScanner();
        ScanCallback callback = new ScanCallback() {
            @Override
            public void onScanFailed(int errorCode) {
                showError("Could not scan BLE", BleCalibrationActivity.this);
            }

            @Override
            public void onScanResult(int callbackType, ScanResult result) {
                Pair<Boolean, Integer> isBeaconPattern = isBeaconPattern(result);
                if(!isBeaconPattern.first) {
                    return;
                }
                final Beacon beacon = createBeaconFromScanRecord(result.getScanRecord().getBytes(), isBeaconPattern.second);
                String id = Long.toString(beacon.getUUID().getLeastSignificantBits());
                if(!emitterId.equals(id)) {
                    return;
                }

                ProgressBar progressBar = signalEmitterCard.findViewById(R.id.signalEmitterCardProgressBar);
                progressBar.setMax(SAMPLE_SIZE);

                if(signalEmitters.get(id).size() >= SAMPLE_SIZE) {
                    //We have old info, reset
                    signalEmitters.put(id, new ArrayList<>());
                }

                signalEmitters.get(id).add(result.getRssi());
                progressBar.setProgress(signalEmitters.get(id).size());

                if(signalEmitters.get(id).size() == SAMPLE_SIZE) {
                    scanner.stopScan(this);
                    updateSignalEmitterInServer(id);
                }
            }
        };
        scanner.startScan(callback);
    }

    public void startCalibration(View calibrateButton) {
        executeAsync(
                () -> locationSystem.getEmitterManager().getSignalEmitters(),
                newCallback(
                        s -> {
                            signalEmitters = new HashMap<>();
                            s.getResult().keySet().forEach(id -> signalEmitters.put(id, new ArrayList<>()));
                            signalEmittersAdapter.setSignalEmitters(new ArrayList<>(signalEmitters.keySet()));
                            signalEmittersAdapter.notifyDataSetChanged();
                        },
                        f -> showError(f.errorMessage(), this)
                )
        );
    }

    private void updateSignalEmitterInServer(String id) {
        try {
            List<Integer> measurements = signalEmitters.get(id);
            int mean = (int)bestValueFrom(measurements);
            Response response = updateSignalEmitter(id, mean, systemConfiguration);
            if(!response.isSuccessful()) {
                terminate(response.body().string());
            }
            showError(format("Updated SE: %s, with TX value: %d", id, mean), this);
        }catch (AsyncTaskException | IOException e) {
            terminate(e.getMessage());
        }
    }

}
