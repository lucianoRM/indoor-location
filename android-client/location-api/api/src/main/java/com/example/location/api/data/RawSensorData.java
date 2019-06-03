package com.example.location.api.data;

import java.util.HashMap;
import java.util.Map;

/**
 * Raw data as the sensor received it
 */
public class RawSensorData {

    private String emitterId;
    private float sensedValue;
    private Map<String, Object> attributes;

    public RawSensorData(String emitterId, float sensedValue) {
        this.emitterId = emitterId;
        this.sensedValue = sensedValue;
        this.attributes = new HashMap<>();
    }

    public void setSensedValue(float sensedValue) {
        this.sensedValue = sensedValue;
    }

    public void setEmitterId(String emitterId) {
        this.emitterId = emitterId;
    }

    public void setAttributes(Map<String, Object> attributes) {
        this.attributes = attributes;
    }

    public void addAttributes(Map<String, Object> attributes) {
        this.attributes.putAll(attributes);
    }

    public void addAttribute(String key, Object value) {
        this.attributes.put(key, value);
    }

    public String getEmitterId() {
        return this.emitterId;
    }

    public float getSensedValue() {
        return this.sensedValue;
    }

    public Map<String, Object> getAttributes() {
        return this.attributes;
    }

}
