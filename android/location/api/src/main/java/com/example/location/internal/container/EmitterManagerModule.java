package com.example.location.internal.container;

import com.example.location.api.system.EmitterManager;
import com.example.location.internal.system.DefaultEmitterManager;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;

@Module
public class EmitterManagerModule {

    @Provides
    @Singleton
    public EmitterManager emitterManager(DefaultEmitterManager emitterManagerImpl) {
        return emitterManagerImpl;
    }

}
