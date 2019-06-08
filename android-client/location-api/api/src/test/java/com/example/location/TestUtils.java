package com.example.location;

import org.apache.commons.io.IOUtils;

import java.io.IOException;
import java.io.InputStream;

import static java.nio.charset.StandardCharsets.UTF_8;

public class TestUtils {

    public static String readFile(String location) throws IOException {
        InputStream user = TestUtils.class.getClassLoader().getResourceAsStream(location);
        return IOUtils.toString(user, UTF_8);
    }
}
