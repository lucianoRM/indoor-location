package com.example.location.internal.entity;

import com.example.location.api.data.Position;

public class DefaultUser implements User {

    private String id;
    private String name;
    private Position position;

    public DefaultUser(String id, String name, Position position) {
        this.id = id;
        this.name = name;
        this.position = position;
    }

    @Override
    public String getId() {
        return id;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public Position getPosition() {
        return position;
    }
}
