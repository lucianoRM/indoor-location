package com.example.location.api.entity.emitter;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorManager;

import com.example.location.api.data.Position;
import com.example.location.api.entity.SkeletalUser;
import com.example.location.api.entity.emitter.SignalEmittingUser;

import static android.support.v4.content.ContextCompat.getSystemService;

public class DefaultSignalEmittingUser extends SkeletalUser implements SignalEmittingUser {

    public DefaultSignalEmittingUser(String id, String name, Position position) {
        super(id, name, position);

        SensorManager sensorManager;
        Sensor sensor;

        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        sensor = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE_UNCALIBRATED);
    }

}
