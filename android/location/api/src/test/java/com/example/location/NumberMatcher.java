package com.example.location;

import org.hamcrest.Description;
import org.hamcrest.TypeSafeMatcher;

import static java.lang.Math.abs;

public class NumberMatcher<T extends Number> extends TypeSafeMatcher<T> {

    public static <T extends Number> NumberMatcher<T> closeTo(T expectedNumber) {
        return new NumberMatcher<>(expectedNumber);
    }

    private double allowedDiff = 0.005f;
    private T expectedNumber;

    private NumberMatcher(T expectedNumber) {
        this.expectedNumber = expectedNumber;
    }

    @Override
    protected void describeMismatchSafely(T item, Description mismatchDescription) {
        mismatchDescription.appendText("got: " + item);
    }

    @Override
    protected boolean matchesSafely(T item) {
        return abs(expectedNumber.doubleValue() - item.doubleValue()) <= allowedDiff;
    }

    @Override
    public void describeTo(Description description) {
        description.appendText("expected: " + expectedNumber);
    }
}
