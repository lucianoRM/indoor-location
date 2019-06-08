package com.example.location.functional;

import com.example.location.api.data.RawSensorData;
import com.example.location.api.entity.sensor.SensorFeed;

import java.util.List;

import static java.util.Collections.emptyList;

/**
 * {@link SensorFeed} that allow for setting a static list of {@link RawSensorData} to later return
 */
public class StaticSensorFeed implements SensorFeed {

    private List<RawSensorData> data = emptyList();

    public void setData(List<RawSensorData> rawSensorData) {
        this.data = rawSensorData;
    }

    @Override
    public List<RawSensorData> getData() {
        return data;
    }
}
