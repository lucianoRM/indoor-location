package com.example.location.api.entity.sensor;

import com.example.location.api.data.DataTransformer;

import static com.google.common.base.Preconditions.checkArgument;
import static java.util.UUID.randomUUID;

public final class SensorConfiguration {

    private String sensorId;
    private String sensorName;
    private SensorFeed sensorFeed;
    private DataTransformer sensedDataTransformer;

    private SensorConfiguration(String sensorId,
                                String sensorName,
                                SensorFeed sensorFeed,
                                DataTransformer sensedDataTransformer) {
        this.sensorId = sensorId;
        this.sensorName = sensorName;
        this.sensorFeed = sensorFeed;
        this.sensedDataTransformer = sensedDataTransformer;
    }

    public static Builder sensorConfigurationBuilder() {
        return new Builder();
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

    public DataTransformer getDataTransformer() {
        return sensedDataTransformer;
    }

    public static class Builder {

        private String sensorId;
        private String sensorName;
        private SensorFeed sensorFeed;
        private DataTransformer sensedDataTransformer;

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

        public Builder withTransformer(DataTransformer dataTransformer) {
            this.sensedDataTransformer = dataTransformer;
            return this;
        }

        public SensorConfiguration build() {
            checkArgument(sensorFeed != null, "Can't create a Sensor without a SensorFeed");
            checkArgument(sensedDataTransformer != null, "Need to configure a DataTransformer for the Sensor");
            if(sensorId == null) {
                sensorId = randomUUID().toString();
            }
            if(sensorName == null) {
                sensorName = sensorId;
            }
            return new SensorConfiguration(sensorId, sensorName, sensorFeed, sensedDataTransformer);
        }

    }
}
