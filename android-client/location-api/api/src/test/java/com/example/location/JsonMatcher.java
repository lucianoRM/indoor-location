package com.example.location;

import com.google.gson.JsonElement;
import com.google.gson.JsonParser;

import org.hamcrest.Description;
import org.hamcrest.TypeSafeMatcher;

public class JsonMatcher extends TypeSafeMatcher<String> {

    public static JsonMatcher sameJson(String expectedJson) {
        return new JsonMatcher(expectedJson);
    }

    private static final JsonParser PARSER = new JsonParser();

    private String expectedJson;

    private JsonMatcher(String expectedJson) {
        this.expectedJson = expectedJson;
    }

    @Override
    protected void describeMismatchSafely(String item, Description mismatchDescription) {
        mismatchDescription.appendText("got: " + item);
    }

    @Override
    protected boolean matchesSafely(String item) {
        JsonElement expected = PARSER.parse(expectedJson);
        JsonElement actual = PARSER.parse(item);
        return expected.equals(actual);
    }

    @Override
    public void describeTo(Description description) {
        description.appendText("expected: " + expectedJson);
    }
}
