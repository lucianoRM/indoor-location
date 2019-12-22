package com.example.location.functional;

import com.example.location.api.system.SystemConfiguration;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.BeforeClass;

import okhttp3.mockwebserver.MockWebServer;
import okhttp3.mockwebserver.RecordedRequest;

import static com.example.location.api.system.SystemConfigurationBuilder.systemConfigurationBuilder;
import static java.util.concurrent.TimeUnit.MILLISECONDS;

public class MockedServerFunctionalTestCase extends AbstractFunctionalTestCase {

    private static final int PORT = 8082;
    private static MockWebServer mockWebServer;

    @BeforeClass
    public static void setUpClass() throws Exception{
        mockWebServer = new MockWebServer();
        mockWebServer.start(PORT);
    }

    @After
    public void tearDown() throws Exception{
        while(true) {
            //empty queue
            RecordedRequest request = mockWebServer.takeRequest(100, MILLISECONDS);
            if(request == null) {
                break;
            }
        }
    }

    @AfterClass
    public static void tearDownClass() throws Exception{
       mockWebServer.close();
    }

    @Override
    protected SystemConfiguration getSystemConfig() {
        return systemConfigurationBuilder()
                .withUserId(USER_ID)
                .withServerIp("localhost")
                .withServerPort(PORT)
                .build();
    }

    protected MockWebServer getMockedServer() {
        return mockWebServer;
    }
}
