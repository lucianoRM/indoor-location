package com.example.location.internal.http;

public enum HttpCode {

    OK(200),

    BAD_REQUEST(400),
    NOT_FOUND(404),
    CONFLICT(409),

    SERVER_ERROR(500);

    private final int code;

    HttpCode(int code) {
        this.code = code;
    }

    public static HttpCode codeFrom(int code) {
        for(HttpCode httpCode : values()) {
            if(httpCode.code == code) {
                return httpCode;
            }
        }
        throw new RuntimeException("I don't know how to react to the response code: " + code);
    }

}
