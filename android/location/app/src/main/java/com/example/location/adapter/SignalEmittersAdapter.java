package com.example.location.adapter;

import android.support.annotation.NonNull;
import android.support.v7.widget.CardView;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.example.location.R;

import java.util.ArrayList;
import java.util.List;

public class SignalEmittersAdapter extends RecyclerView.Adapter<SignalEmittersAdapter.SignalEmitterViewHolder> {

    private List<String> signalEmitters;

    public SignalEmittersAdapter() {
        this.signalEmitters = new ArrayList<>();
    }

    public void setSignalEmitters(List<String> signalEmitters) {
        this.signalEmitters = signalEmitters;
    }

    @NonNull
    @Override
    public SignalEmitterViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        LayoutInflater inflater = LayoutInflater.from(viewGroup.getContext());
        View view = inflater.inflate(R.layout.signal_emitter_card_layout, viewGroup, false);
        return new SignalEmitterViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull SignalEmitterViewHolder signalEmitterViewHolder, int i) {
        String emitterId = signalEmitters.get(i);
        signalEmitterViewHolder.setId(emitterId);
    }

    @Override
    public int getItemCount() {
        return signalEmitters.size();
    }

    public static class SignalEmitterViewHolder extends RecyclerView.ViewHolder{

        final TextView emitterId;
        final ProgressBar progressBar;

        public void setId(String id) {
            emitterId.setText(id);
            progressBar.setProgress(0);
        }

        public SignalEmitterViewHolder(@NonNull View itemView) {
            super(itemView);
            CardView cardView = itemView.findViewById(R.id.signalEmitterCardView);
            emitterId =  cardView.findViewById(R.id.signalEmitterIdCardTextView);
            progressBar =  cardView.findViewById(R.id.signalEmitterCardProgressBar);
            progressBar.setProgress(0);
        }
    }
}
