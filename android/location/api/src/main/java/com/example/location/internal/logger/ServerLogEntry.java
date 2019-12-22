package com.example.location.internal.logger;

public class ServerLogEntry {

    private final String tag;
    private final String message;

    public static ServerLogEntry entry(String tag, String message) {
        return new ServerLogEntry(tag, message);
    }

    private ServerLogEntry(String tag, String message) {
        this.tag = tag;
        this.message = message;
    }

    public String getTag() {
        return tag;
    }

    public String getMessage() {
        return message;
    }
}
