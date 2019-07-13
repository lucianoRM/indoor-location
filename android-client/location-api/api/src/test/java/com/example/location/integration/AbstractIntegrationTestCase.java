package com.example.location.integration;

import com.example.location.api.data.Position;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.functional.AbstractFunctionalTestCase;

import org.junit.After;
import org.junit.Before;

import java.io.File;
import java.io.IOException;
import java.util.Map;

import okhttp3.MediaType;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import static com.example.location.internal.http.HttpCode.OK;
import static com.example.location.internal.http.HttpCode.codeFrom;
import static com.example.location.internal.http.HttpLocationClient.ANCHORS_ENDPOINT;
import static com.example.location.internal.http.HttpLocationClient.MY_SENSORS_ENDPOINT;
import static com.example.location.internal.http.HttpLocationClient.USERS_ENDPOINT;
import static java.lang.Runtime.getRuntime;
import static java.lang.String.format;
import static java.lang.System.getProperty;
import static java.lang.Thread.sleep;
import static okhttp3.MediaType.get;
import static org.apache.commons.io.IOUtils.copy;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.MatcherAssert.assertThat;

public class AbstractIntegrationTestCase extends AbstractFunctionalTestCase {

    //TODO: FIX THIS
    private static final String ROOT_FOLDER_SYSTEM_PROPERTY = "user.dir";
    private static final String API_EXECUTABLE_LOCATION = "server/api.py";
    private static final String FLASK_EXECUTABLE_LOCATION = "server/venv3/bin/flask";

    private static final int THREAD_WAITING_TIME = 1000;

    private static final String ANCHOR_TEMPLATE =
            "{" +
                    "\"id\": \"%s\"," +
                    " \"position\" : {\"x\":%f, \"y\":%f}" +
                    "}";

    private static final String SERVER_START_COMMAND;
    private static final String SERVER_ENVIRONMENT_VARIABLE;

    static {
        try {
            File rootFolder = new File(getProperty(ROOT_FOLDER_SYSTEM_PROPERTY));
            File serverRootFolder = rootFolder.getParentFile().getParentFile().getParentFile();
            File apiFile = new File(serverRootFolder, API_EXECUTABLE_LOCATION);
            File flaskFile = new File(serverRootFolder, FLASK_EXECUTABLE_LOCATION);

            SERVER_ENVIRONMENT_VARIABLE = "FLASK_APP=" + apiFile.getAbsolutePath();
            SERVER_START_COMMAND = flaskFile.getAbsolutePath() + " run";
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private Process serverProcess;
    private Thread readingThread;
    private Thread errorThread;

    @Before
    public void setUp() throws Exception {
        serverProcess = getRuntime().exec(SERVER_START_COMMAND, new String[]{SERVER_ENVIRONMENT_VARIABLE});
        readingThread = new Thread(() -> {
            while (!readingThread.isInterrupted()) {
                try {
                    copy(serverProcess.getInputStream(), System.out);
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            }
        });
        errorThread = new Thread(() -> {
            while (!errorThread.isInterrupted()) {
                try {
                    copy(serverProcess.getErrorStream(), System.out);
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            }
        });
        errorThread.start();
        readingThread.start();

        //wait for server to start
        sleep(2000);

        super.setUp();
        //register user in server
        MediaType json = get("application/json");
        String user = format("{\"id\":\"%s\"}", USER_ID);
        RequestBody requestBody = RequestBody.create(json, user);
        Request request = new Request.Builder().url(getServerUrl() + USERS_ENDPOINT).post(requestBody).build();
        Response response = httpClient().newCall(request).execute();
        assertThat(codeFrom(response.code()), is(equalTo(OK)));
    }

    @After
    public void tearDown() {
        errorThread.interrupt();
        readingThread.interrupt();

        serverProcess.destroy();

        try {
            errorThread.join(THREAD_WAITING_TIME);
            readingThread.join(THREAD_WAITING_TIME);
        } catch (InterruptedException e) {
            throw new RuntimeException("could not stop reading process threads", e);
        }
    }

    private void executeRequest(Request request) throws IOException{
        Response response = httpClient().newCall(request).execute();
        assertThat(codeFrom(response.code()), is(equalTo(OK)));
    }

    protected String createAnchor(String id, Position position) {
        return format(ANCHOR_TEMPLATE, id, position.getX(), position.getY());
    }

    protected void registerAnchorInServer(String anchor) throws IOException {
        MediaType json = get("application/json");
        RequestBody requestBody = RequestBody.create(json, anchor);
        Request request = new Request.Builder().url(getServerUrl() + ANCHORS_ENDPOINT).post(requestBody).build();
        executeRequest(request);
    }

    protected void registerSignalEmitterInAnchor(String anchorId, SignalEmitter signalEmitter) throws IOException {
        MediaType json = get("application/json");
        RequestBody requestBody = RequestBody.create(json, getGson().toJson(signalEmitter));
        String endpoint = getServerUrl() + ANCHORS_ENDPOINT + "/" + anchorId + "/signal_emitters";
        Request request = new Request.Builder().url(endpoint).post(requestBody).build();
        executeRequest(request);
    }

    protected Position findMe() throws IOException {
        Request request = new Request.Builder().url(getServerUrl() + USERS_ENDPOINT + "/" + USER_ID).get().build();
        Response response = httpClient().newCall(request).execute();
        Map user = getGson().fromJson(response.body().string(), Map.class);
        Map<String, Double> position = (Map<String, Double>)user.get("position");
        return new Position(position.get("x").floatValue(), position.get("y").floatValue());
    }

    protected Sensor getSensorFromServer(String id) throws IOException {
        Request request = new Request.Builder().url(getServerUrl() + MY_SENSORS_ENDPOINT + "/" + id).get().build();
        Response response = httpClient().newCall(request).execute();
        return getGson().fromJson(response.body().string(), Sensor.class);
    }

}
