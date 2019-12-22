package com.example.location.internal.container;

import java.util.concurrent.ExecutorService;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;

import static java.util.concurrent.Executors.newFixedThreadPool;


@Module
public class ExecutorServiceModule {

    private static final int THREADS = 1;

    @Singleton
    @Provides
    public ExecutorService executorService() {
        return newFixedThreadPool(THREADS);
    }
}
