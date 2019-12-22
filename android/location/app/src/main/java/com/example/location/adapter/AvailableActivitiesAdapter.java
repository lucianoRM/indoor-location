package com.example.location.adapter;

import android.support.annotation.NonNull;
import android.support.v7.widget.CardView;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.example.location.R;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;


public class AvailableActivitiesAdapter extends RecyclerView.Adapter<AvailableActivitiesAdapter.AvailableActivityViewHolder> {

    private List<String> availableActivities;

    public AvailableActivitiesAdapter(List<String> availableActivities) {
        this.availableActivities = availableActivities;
    }

    @NonNull
    @Override
    public AvailableActivityViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        LayoutInflater inflater = LayoutInflater.from(viewGroup.getContext());
        View view = inflater.inflate(R.layout.activity_card_layout, viewGroup, false);
        return new AvailableActivityViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull AvailableActivityViewHolder activityViewHolder, int i) {
        String activityName = availableActivities.get(i);
        activityViewHolder.setName(activityName);
    }

    @Override
    public int getItemCount() {
        return availableActivities.size();
    }

    public static class AvailableActivityViewHolder extends RecyclerView.ViewHolder{

        final TextView activityName;

        public void setName(String name) {
            activityName.setText(name);
        }

        public AvailableActivityViewHolder(@NonNull View itemView) {
            super(itemView);
            CardView cardView = itemView.findViewById(R.id.activityCardView);
            activityName =  cardView.findViewById(R.id.activityName);
        }
    }
}
