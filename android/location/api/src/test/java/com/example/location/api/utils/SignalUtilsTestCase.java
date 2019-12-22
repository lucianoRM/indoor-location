package com.example.location.api.utils;

import org.junit.Test;

import java.util.ArrayList;

import static com.example.location.api.utils.SensingUtils.bestValueFrom;
import static java.util.Arrays.asList;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.closeTo;
import static org.hamcrest.Matchers.is;

public class SignalUtilsTestCase {

    @Test
    public void valueFromEmptyList() {
        assertThat(bestValueFrom(new ArrayList<Integer>()), is(0.0));
    }

    @Test
    public void valueFrom2ElementList() {
        assertThat(bestValueFrom(asList(2,4)),is(3.0));
    }
     

    @Test
    public void valueFromCompleteList() {
        assertThat(bestValueFrom(asList(
                -4,4,-5,5,-1000,-200,-1,1,408,0
        )),is(closeTo(0.0, 0.0001)));
    }
}



