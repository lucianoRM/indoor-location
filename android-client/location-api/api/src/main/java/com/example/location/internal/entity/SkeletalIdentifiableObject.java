package com.example.location.internal.entity;

import java.util.Objects;

public abstract class SkeletalIdentifiableObject implements IdentifiableObject {

    private String id;
    private String name;

    public SkeletalIdentifiableObject(String id, String name) {
        this.id = id;
        this.name = name;
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name);
    }

    @Override
    public boolean equals(Object obj) {
        if(!(obj instanceof SkeletalIdentifiableObject)) {
            return false;
        }
        if(obj == this) {
            return true;
        }
        SkeletalIdentifiableObject other = (SkeletalIdentifiableObject) obj;
        return this.id.equals(other.id) && this.name.equals(other.name);
    }

    @Override
    public String toString() {
        return getId() + "(" + getName() + ")";
    }
}
