package com.example.location.integration;

import com.example.location.api.data.DataTransformer;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.entity.sensor.SensorFeed;
import com.example.location.functional.AbstractFunctionalTestCase;
import com.example.location.functional.StaticSensorFeed;
import com.example.location.functional.TestDataTransformer;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.File;

import static com.example.location.api.entity.sensor.SensorConfiguration.sensorConfigurationBuilder;
import static java.lang.Runtime.getRuntime;
import static java.lang.System.getProperty;
import static java.lang.Thread.sleep;
import static org.apache.commons.io.IOUtils.copy;

public class AbstractIntegrationTestCase extends AbstractFunctionalTestCase {

    private static final int PORT = 5000;

    //TODO: FIX THIS
    private static final String ROOT_FOLDER_SYSTEM_PROPERTY = "user.dir";
    private static final String API_EXECUTABLE_LOCATION = "server/api.py";
    private static final String FLASK_EXECUTABLE_LOCATION = "server/venv3/bin/flask";

    private static final int THREAD_WAITING_TIME = 1000;

    private static final String SERVER_START_COMMAND;
    private static final String SERVER_ENVIRORMENT_VARIABLE;
    static {
        try {
            File rootFolder = new File(getProperty(ROOT_FOLDER_SYSTEM_PROPERTY));
            File serverRootFolder = rootFolder.getParentFile().getParentFile().getParentFile();
            File apiFile = new File(serverRootFolder, API_EXECUTABLE_LOCATION);
            File flaskFile =  new File(serverRootFolder, FLASK_EXECUTABLE_LOCATION);

            SERVER_ENVIRORMENT_VARIABLE = "FLASK_APP=" + apiFile.getAbsolutePath();
            SERVER_START_COMMAND = flaskFile.getAbsolutePath() + " run";
        }catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private Process serverProcess;
    private Thread readingThread;
    private Thread errorThread;

    @Before
    public void setUp() throws Exception{
        super.setUp();
        serverProcess = getRuntime().exec(SERVER_START_COMMAND, new String[]{SERVER_ENVIRORMENT_VARIABLE});
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

    @Test
    public void test() {
        final SensorFeed feed = new StaticSensorFeed();
        final DataTransformer transformer = new TestDataTransformer();
        Sensor sensor = getContainer().sensorManager().createSensor(sensorConfigurationBuilder()
                .withId("id")
                .withName("name")
                .withFeed(feed)
                .withTransformer(transformer)
                .build());
    }

}
