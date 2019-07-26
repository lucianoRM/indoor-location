package com.example.location.internal.container;

import com.example.location.api.system.Locator;
import com.example.location.internal.system.DefaultLocator;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;

@Module
public class LocatorModule {

    @Provides
    @Singleton
    public Locator locator(DefaultLocator defaultLocator) {
        return defaultLocator;
    }

}
