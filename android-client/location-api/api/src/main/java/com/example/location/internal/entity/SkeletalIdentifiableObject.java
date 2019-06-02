package com.example.location.internal.entity;

import com.example.location.api.data.Position;

import java.util.Objects;

public abstract class SkeletalIdentifiableObject implements IdentifiableObject {

    private String id;
    private String name;
    private Position position;

    public SkeletalIdentifiableObject(String id, String name, Position position) {
        this.id = id;
        this.name = name;
        this.position = position;
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Position getPosition() {
        return position;
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name, position);
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
        return this.id.equals(other.id) && this.name.equals(other.name) && this.position.equals(other.position);
    }

    @Override
    public String toString() {
        return getId() + "(" + getName() + ")@" + getPosition().getX() + "-" + getPosition().getY();
    }
}
