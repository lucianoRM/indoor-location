package com.example.location;

import com.example.location.internal.entity.IdentifiableObject;

import org.hamcrest.Description;
import org.hamcrest.TypeSafeMatcher;

public class IdentifiableObjectMatcher extends TypeSafeMatcher<IdentifiableObject> {

    public static IdentifiableObjectMatcher sameAs(IdentifiableObject identifiableObject) {
        return new IdentifiableObjectMatcher(identifiableObject);
    }

    private IdentifiableObject expectedObject;

    private IdentifiableObjectMatcher(IdentifiableObject expectedObject) {
        this.expectedObject = expectedObject;
    }

    @Override
    protected void describeMismatchSafely(IdentifiableObject item, Description mismatchDescription) {
        mismatchDescription.appendText("got: " + item);
    }

    @Override
    protected boolean matchesSafely(IdentifiableObject item) {
        return this.expectedObject.equals(item);
    }

    @Override
    public void describeTo(Description description) {
        description.appendText("expected: " + expectedObject);
    }
}
