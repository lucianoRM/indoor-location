package com.example.location.internal;

import java.util.function.Consumer;

@FunctionalInterface
public interface ThrowingConsumer<T, E extends Throwable> extends Consumer<T> {

    default void accept(T obj) {
        try {
            getThrows(obj);
        } catch (Throwable e) {
            throw new RuntimeException(e);
        }
    }

    void getThrows(T obj) throws E;

}
