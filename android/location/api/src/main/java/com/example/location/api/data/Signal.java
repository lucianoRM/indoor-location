package com.example.location.api.data;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

import static java.util.Optional.ofNullable;

/**
 * Models the Signal being emitted by a {@link com.example.location.api.entity.emitter.SignalEmitter}.
 */
public class Signal {

    private Map<String, String> attributes = new HashMap<>();

    public void addAttribute(String key, String attribute) {
        attributes.put(key, attribute);
    }

    public Optional<String> getAttribute(String key) {
        return ofNullable(attributes.get(key));
    }

    @Override
    public String toString() {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("{ ");
        attributes.forEach((k,v) -> stringBuilder.append(k + ":" + v + " "));
        stringBuilder.append("}");
        return stringBuilder.toString();
    }

    @Override
    public int hashCode() {
        return attributes.hashCode();
    }

    @Override
    public boolean equals(Object obj) {
        if(obj == null) {
            return false;
        }
        if(!(obj instanceof Signal)) {
           return false;
        }
        return attributes.equals(((Signal)obj).attributes);
    }
}
