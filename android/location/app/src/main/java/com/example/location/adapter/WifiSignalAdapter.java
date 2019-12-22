package com.example.location.adapter;

import android.net.wifi.ScanResult;
import android.support.annotation.NonNull;
import android.support.v7.widget.CardView;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.example.location.R;

import java.util.List;

import static com.example.location.impl.SignalUtils.computeDistance;
import static java.lang.String.format;

public class WifiSignalAdapter extends RecyclerView.Adapter<WifiSignalAdapter.WifiSignalViewHolder> {

    private List<ScanResult> scanResults;

    public WifiSignalAdapter(List<ScanResult> scanResults) {
        this.scanResults = scanResults;
    }

    @NonNull
    @Override
    public WifiSignalViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        LayoutInflater inflater = LayoutInflater.from(viewGroup.getContext());
        View view = inflater.inflate(R.layout.signal_card_layout, viewGroup, false);
        return new WifiSignalViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull WifiSignalViewHolder wifiSignalViewHolder, int i) {
        ScanResult scanResult = scanResults.get(i);
        wifiSignalViewHolder.populate(scanResult);
    }

    @Override
    public int getItemCount() {
        return scanResults.size();
    }

    public static class WifiSignalViewHolder extends RecyclerView.ViewHolder {

        final TextView signalName;
        final TextView signalLevel;
        final TextView signalDistance;

        public WifiSignalViewHolder(@NonNull View itemView) {
            super(itemView);
            CardView cardView = itemView.findViewById(R.id.signalCardView);
            signalName =  cardView.findViewById(R.id.signalName);
            signalLevel = cardView.findViewById(R.id.signalLevel);
            signalDistance = cardView.findViewById(R.id.signalDistance);
        }

        private void populate(ScanResult scanResult) {
            this.signalName.setText(scanResult.SSID);
            this.signalLevel.setText(format("%d dBm",scanResult.level));

            double myDistance = computeDistance(scanResult.level, -23.0f , 4.0f);

            this.signalDistance.setText(format("%.2f m",myDistance));

        }
    }

}
