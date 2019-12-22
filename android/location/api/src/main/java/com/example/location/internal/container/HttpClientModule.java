package com.example.location.internal.container;


import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.Request;

import static com.example.location.internal.http.HttpLocationClient.USER_ID_PLACEHOLDER;


@Module
public class HttpClientModule {

    private String userId;

    public HttpClientModule(String userId) {
        this.userId = userId;
    }

    @Provides
    @Singleton
    public OkHttpClient httpClient() {
        return new OkHttpClient.Builder().addInterceptor(
                chain -> {
                    Request request = chain.request();
                    int placeholderPosition = request.url().pathSegments().indexOf(USER_ID_PLACEHOLDER);
                    if (placeholderPosition >= 0) {
                        HttpUrl url = request.url().newBuilder().setPathSegment(placeholderPosition, userId).build();
                        request = request.newBuilder().url(url).build();
                    }
                    return chain.proceed(request);
                }).build();
    }
}
