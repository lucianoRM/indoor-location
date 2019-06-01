package com.example.location.api.entity.sensor;

public class SensorConfiguration {

    private String sensorId;
    private String sensorName;
    private SensorFeed sensorFeed;

    public SensorConfiguration(String sensorId, String sensorName, SensorFeed sensorFeed) {
        this.sensorId = sensorId;
        this.sensorName = sensorName;
        this.sensorFeed = sensorFeed;
    }

    public String getSensorId() {
        return sensorId;
    }

    public String getSensorName() {
        return sensorName;
    }

    public SensorFeed getSensorFeed() {
        return sensorFeed;
    }

    public static class Builder {

        private String sensorId;
        private String sensorName;
        private SensorFeed sensorFeed;

        public Builder withId(String sensorId) {
            this.sensorId = sensorId;
            return this;
        }

        public Builder withName(String sensorName) {
            this.sensorName = sensorName;
            return this;
        }

        public Builder withFeed(SensorFeed sensorFeed) {
            this.sensorFeed = sensorFeed;
            return this;
        }

        public SensorConfiguration build() {
            return new SensorConfiguration(sensorId, sensorName, sensorFeed);
        }

    }
}
