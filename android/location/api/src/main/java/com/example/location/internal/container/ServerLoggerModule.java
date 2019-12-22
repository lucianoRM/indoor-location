package com.example.location.internal.container;

import com.example.location.internal.logger.DefaultServerLogger;
import com.example.location.internal.logger.ServerLogger;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;

@Module
public class ServerLoggerModule {

    @Singleton
    @Provides
    public ServerLogger serverLogger(DefaultServerLogger serverLoggerImpl) {
        return serverLoggerImpl;
    }

}
