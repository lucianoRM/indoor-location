package com.example.location.api.entity;

import com.example.location.api.data.Position;

import java.util.Objects;

public abstract class SkeletalUser implements User {

    private String id;
    private String name;
    private Position position;

    public SkeletalUser(String id, String name, Position position) {
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
        if(!(obj instanceof SkeletalUser)) {
            return false;
        }
        if(obj == this) {
            return true;
        }
        SkeletalUser other = (SkeletalUser) obj;
        return this.id.equals(other.id) && this.name.equals(other.name) && this.position.equals(other.position);
    }
}
