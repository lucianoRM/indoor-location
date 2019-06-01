package com.example.location;

import com.example.location.api.data.Position;
import com.example.location.internal.entity.SkeletalUser;
import com.example.location.api.entity.User;

import org.hamcrest.Description;
import org.hamcrest.TypeSafeMatcher;

public class UserMatcher extends TypeSafeMatcher<User> {

    public static UserMatcher user(String id, String name, float x, float y) {
        return new UserMatcher(id, name, new Position(x,y));
    }

    public static UserMatcher user(User user) {
        return new UserMatcher(user);
    }

    private User expectedUser;

    private UserMatcher(User expectedUser) {
        this.expectedUser = expectedUser;
    }

    private UserMatcher(String expectedId, String expectedName, Position expectedPosition) {
        this.expectedUser = new SkeletalUser(expectedId, expectedName, expectedPosition) {};
    }

    @Override
    protected void describeMismatchSafely(User item, Description mismatchDescription) {
        mismatchDescription.appendText("got: " + item);
    }

    @Override
    protected boolean matchesSafely(User item) {
        return this.expectedUser.equals(item);
    }

    @Override
    public void describeTo(Description description) {
        description.appendText("expected: " + expectedUser);
    }
}
