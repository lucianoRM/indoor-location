package com.example.location.activity;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.Button;

import com.example.location.R;
import com.example.location.adapter.WifiSignalAdapter;

import static android.graphics.Color.GREEN;
import static android.graphics.Color.RED;

public class WifiSignalViewActivity extends AppCompatActivity {

    private WifiManager wifiManager;
    private RecyclerView wifiRecyclerView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_wifi_signal_view);
        this.wifiManager = (WifiManager) getSystemService(WIFI_SERVICE);

        RecyclerView recyclerView = findViewById(R.id.wifiNetworksRecyclerView);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(new WifiSignalAdapter(wifiManager.getScanResults()));
        this.wifiRecyclerView = recyclerView;

        registerScanReceiver();
    }

    private void populateCards() {
        WifiSignalAdapter adapter = new WifiSignalAdapter(wifiManager.getScanResults());
        wifiRecyclerView.setAdapter(adapter);
    }


    private void registerScanReceiver() {
        BroadcastReceiver wifiScanReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context c, Intent intent) {
                boolean success = intent.getBooleanExtra(WifiManager.EXTRA_RESULTS_UPDATED, false);
                if (success) {
                    scanSuccess();
                } else {
                    // scan failure handling
                    scanFailure();
                }
            }
        };
        IntentFilter intentFilter = new IntentFilter();
        intentFilter.addAction(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION);
        registerReceiver(wifiScanReceiver, intentFilter);
    }

    public void scanNetworks(View view) {
        Button resetButton = view.findViewById(R.id.reset);
        resetButton.setBackgroundColor(Color.GRAY);

        boolean scanResult = wifiManager.startScan();
        if(scanResult) {
            scanSuccess();
        }else {
            scanFailure();
        }
    }


    private void scanSuccess() {
        populateCards();
        findViewById(R.id.reset).setBackgroundColor(GREEN);
    }

    private void scanFailure() {
        populateCards();
        findViewById(R.id.reset).setBackgroundColor(RED);
    }

}
