package com.example.location.task;

import android.os.AsyncTask;

import com.example.location.api.system.SystemConfiguration;

import java.util.Optional;
import java.util.concurrent.Callable;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import static com.example.location.impl.RadioDataTransformer.MEDIUM_COEFFICIENT_SIGNAL_KEY;
import static com.example.location.impl.RadioDataTransformer.ONE_METER_POWER_SIGNAL_KEY;
import static com.example.location.activity.SettingsActivity.MEDIUM_COEF_ATTRIBUTE;
import static java.lang.String.format;
import static java.util.concurrent.TimeUnit.MILLISECONDS;
import static okhttp3.MediaType.get;

public class HttpUtils {

    //TODO: Make this configurable
    private static final long DEFAULT_TIMEOUT_MILLIS = 5000;

    private static final OkHttpClient httpClient = new OkHttpClient();

    public static Response registerUser(SystemConfiguration systemConfiguration) throws AsyncTaskException{
        return requestBlocking( () -> {
            MediaType json = get("application/json");
            String user = format("{\"id\":\"%s\"}", systemConfiguration.getUserId());
            RequestBody requestBody = RequestBody.create(json, user);
            Request request = new Request.Builder().url(buildUrl(systemConfiguration, "/users")).post(requestBody).build();
            return httpClient.newCall(request).execute();
        });
    }

    public static Response deleteAnchor(String anchorId, SystemConfiguration systemConfiguration) throws AsyncTaskException {
        return requestBlocking(() -> {
            Request request = new Request.Builder().url(buildUrl(systemConfiguration, format("/anchors/%s", anchorId))).delete().build();
            return httpClient.newCall(request).execute();
        });
    }

    public static Response registerAnchor(String anchorId, float x, float y, SystemConfiguration systemConfiguration) throws AsyncTaskException{
        return requestBlocking(() -> {
            MediaType json = get("application/json");
            String anchor = format("{\"id\":\"%s\", \"position\" : {\"x\" : %f , \"y\" : %f}}", anchorId, x, y);
            RequestBody requestBody = RequestBody.create(json, anchor);
            Request request = new Request.Builder().url(buildUrl(systemConfiguration,"/anchors")).post(requestBody).build();
            return httpClient.newCall(request).execute();
        });

    }

    public static Response addSignalEmitter(String anchorId, String signalEmitterId, Integer oneMeterPower, SystemConfiguration systemConfiguration) throws AsyncTaskException{
        return requestBlocking(() -> {
            float mediumCoefficient = systemConfiguration.getConfigAttribute(MEDIUM_COEF_ATTRIBUTE);
            MediaType json = get("application/json");
            String anchor = format(
                    "{" +
                            "\"id\":\"%s\", " +
                            "\"signal\":{" +
                            "   \"%s\":%d, " +
                            "   \"%s\":%f" +
                            "}" +
                            "}",
                    signalEmitterId,
                    ONE_METER_POWER_SIGNAL_KEY, oneMeterPower,
                    MEDIUM_COEFFICIENT_SIGNAL_KEY, mediumCoefficient);
            RequestBody requestBody = RequestBody.create(json, anchor);
            Request request = new Request.Builder().url(buildUrl(systemConfiguration, format("/anchors/%s/signal_emitters", anchorId))).post(requestBody).build();
            return httpClient.newCall(request).execute();
        });
    }

    public static Response updateSignalEmitter(String signalEmitterId, Integer oneMeterPower, SystemConfiguration systemConfiguration) throws AsyncTaskException {
        return requestBlocking(() -> {
            MediaType json = get("application/json");
            String newSignal = format("{\"%s\":%d}", ONE_METER_POWER_SIGNAL_KEY, oneMeterPower);
            RequestBody requestBody = RequestBody.create(json, newSignal);
            Request request = new Request.Builder().url(buildUrl(systemConfiguration, format("/signal_emitters/%s/signal", signalEmitterId))).put(requestBody).build();
            return httpClient.newCall(request).execute();
        });
    }

    private static String buildUrl(SystemConfiguration systemConfiguration, String resourcePath) {
        return format("http://%s:%d%s", systemConfiguration.getServerHost(), systemConfiguration.getServerPort(), resourcePath);
    }

    private static Response requestBlocking(Callable<Response> request) throws AsyncTaskException{
        LambdaAsyncTask asyncTask = new LambdaAsyncTask(request);
        asyncTask.execute();
        try {
            Response response = asyncTask.get(DEFAULT_TIMEOUT_MILLIS, MILLISECONDS);
            if (asyncTask.getException().isPresent()) {
                throw asyncTask.getException().get();
            }
            return response;
        }catch (Exception e) {
            throw new AsyncTaskException(e);
        }
    }

    private static final class LambdaAsyncTask extends AsyncTask<Void, Void, Response> {

        private Exception exception;
        private Callable<Response> callable;

        private LambdaAsyncTask(Callable<Response> runnable) {
            this.callable = runnable;
        }

        private Optional<Exception> getException() {
            return Optional.ofNullable(exception);
        }

        @Override
        protected Response doInBackground(Void... voids) {
            try {
                return callable.call();
            }catch (Exception e) {
                this.exception = e;
            }
            return null;
        }
    }
}
