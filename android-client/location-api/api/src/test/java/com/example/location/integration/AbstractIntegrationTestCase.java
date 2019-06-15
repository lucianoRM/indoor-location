package com.example.location.integration;

import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.functional.AbstractFunctionalTestCase;

import org.junit.After;
import org.junit.Before;

import java.io.File;
import java.io.IOException;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import static com.example.location.internal.config.StaticSystemConfiguration.config;
import static com.example.location.internal.http.HttpLocationClient.SENSORS_ENDPOINT;
import static com.example.location.internal.http.HttpLocationClient.SIGNAL_EMITTERS_ENDPOINT;
import static java.lang.Runtime.getRuntime;
import static java.lang.System.getProperty;
import static java.lang.Thread.sleep;
import static okhttp3.MediaType.get;
import static org.apache.commons.io.IOUtils.copy;

public class AbstractIntegrationTestCase extends AbstractFunctionalTestCase {

    private static final int PORT = config().getServerPort();

    //TODO: FIX THIS
    private static final String ROOT_FOLDER_SYSTEM_PROPERTY = "user.dir";
    private static final String API_EXECUTABLE_LOCATION = "server/api.py";
    private static final String FLASK_EXECUTABLE_LOCATION = "server/venv3/bin/flask";

    private static final int THREAD_WAITING_TIME = 1000;

    private static final String SERVER_START_COMMAND;
    private static final String SERVER_ENVIRONMENT_VARIABLE;
    static {
        try {
            File rootFolder = new File(getProperty(ROOT_FOLDER_SYSTEM_PROPERTY));
            File serverRootFolder = rootFolder.getParentFile().getParentFile().getParentFile();
            File apiFile = new File(serverRootFolder, API_EXECUTABLE_LOCATION);
            File flaskFile =  new File(serverRootFolder, FLASK_EXECUTABLE_LOCATION);

            SERVER_ENVIRONMENT_VARIABLE = "FLASK_APP=" + apiFile.getAbsolutePath();
            SERVER_START_COMMAND = flaskFile.getAbsolutePath() + " run";
        }catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private OkHttpClient client;
    private Process serverProcess;
    private Thread readingThread;
    private Thread errorThread;

    @Before
    public void setUp() throws Exception{
        super.setUp();

        client = new OkHttpClient();

        serverProcess = getRuntime().exec(SERVER_START_COMMAND, new String[]{SERVER_ENVIRONMENT_VARIABLE});
        readingThread = new Thread(() -> {
            while(!readingThread.isInterrupted()) {
                try {
                    copy(serverProcess.getInputStream(), System.out);
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            }
        });
        errorThread = new Thread(() -> {
            while(!errorThread.isInterrupted()) {
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

    @Override
    protected int getServerPort() {
        return PORT;
    }

    protected void registerSignalEmitterInServer(SignalEmitter signalEmitter) throws IOException{
        MediaType json = get("application/json");
        RequestBody requestBody = RequestBody.create(json, getGson().toJson(signalEmitter));
        Request request = new Request.Builder().url(getServerUrl() + SIGNAL_EMITTERS_ENDPOINT).post(requestBody).build();
        Response response = this.client.newCall(request).execute();
    }

    protected Sensor getSensorFromServer(String id) throws IOException {
        Request request = new Request.Builder().url(getServerUrl() + SENSORS_ENDPOINT + "/" + id).get().build();
        Response response = this.client.newCall(request).execute();
        return getGson().fromJson(response.body().string() ,Sensor.class);
    }

}
