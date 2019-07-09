package com.example.location.internal.container;

import com.example.location.internal.config.SystemConfiguration;
import com.google.gson.Gson;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;
import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.converter.scalars.ScalarsConverterFactory;

import static java.lang.String.format;

@Module
public class RetrofitModule {

    @Provides
    @Singleton
    public Retrofit retrofit(OkHttpClient okHttpClient, Gson gson, SystemConfiguration systemConfiguration) {
        return new Retrofit.Builder()
                .baseUrl(format("%s://%s:%d", systemConfiguration.getServerProtocol(), systemConfiguration.getServerHost(), systemConfiguration.getServerPort()))
                .client(okHttpClient)
                .addConverterFactory(ScalarsConverterFactory.create())
                .addConverterFactory(GsonConverterFactory.create(gson))
                .build();
    }

}
