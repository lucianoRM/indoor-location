package com.example.location.internal.entity;

/**
 * Base interface for every identifiable object in the system
 */
public interface IdentifiableObject {

    /**
     * @return this object's id
     */
    String getId();

    /**
     * @return this object's name
     */
    String getName();

}
