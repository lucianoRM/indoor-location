package com.example.location.adapter;

import android.support.annotation.NonNull;
import android.support.v7.widget.CardView;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.example.location.activity.BleViewActivity;
import com.example.location.R;

import java.util.List;

import static com.example.location.impl.SignalUtils.computeDistance;
import static java.lang.String.format;

public class BleSignalAdapter extends RecyclerView.Adapter<BleSignalAdapter.BLESignalViewHolder> {

    private List<BleViewActivity.BleDevice> bleDevices;

    public BleSignalAdapter(List<BleViewActivity.BleDevice> bleDevices) {
        this.bleDevices = bleDevices;
    }

    @NonNull
    @Override
    public BLESignalViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        LayoutInflater inflater = LayoutInflater.from(viewGroup.getContext());
        View view = inflater.inflate(R.layout.signal_card_layout, viewGroup, false);
        return new BLESignalViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull BLESignalViewHolder bleSignalViewHolder, int i) {
        BleViewActivity.BleDevice bleDevice = bleDevices.get(i);
        bleSignalViewHolder.populate(bleDevice);
    }

    @Override
    public int getItemCount() {
        return bleDevices.size();
    }

    public static class BLESignalViewHolder extends RecyclerView.ViewHolder {

        final TextView signalName;
        final TextView signalLevel;
        final TextView signalDistance;

        public BLESignalViewHolder(@NonNull View itemView) {
            super(itemView);
            CardView cardView = itemView.findViewById(R.id.signalCardView);
            signalName =  cardView.findViewById(R.id.signalName);
            signalLevel = cardView.findViewById(R.id.signalLevel);
            signalDistance = cardView.findViewById(R.id.signalDistance);
        }

        private void populate(BleViewActivity.BleDevice bleDevice) {
            this.signalName.setText(bleDevice.getId());
            this.signalLevel.setText(format("%d dBm",bleDevice.getPower()));

            double myDistance = computeDistance(bleDevice.getPower(), -68.0f , 2.5f);

            this.signalDistance.setText(format("%.2f m",myDistance));

        }
    }

}
