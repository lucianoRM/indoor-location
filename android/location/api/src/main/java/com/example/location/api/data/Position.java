package com.example.location.api.data;

import java.util.Objects;

public class Position {

    private float x;
    private float y;

    public Position(float x, float y) {
        this.x = x;
        this.y = y;
    }

    public float getX() {
        return x;
    }

    public float getY() {
        return y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(this.x, this.y);
    }

    @Override
    public boolean equals(Object obj) {
        if(!(obj instanceof Position)) {
            return false;
        }
        if(obj == this) {
            return true;
        }
        Position other = (Position) obj;
        return this.x == other.x && this.y == other.y;
    }
}
