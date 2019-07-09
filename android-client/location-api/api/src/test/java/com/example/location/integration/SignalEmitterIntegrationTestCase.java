package com.example.location.integration;

import com.example.location.api.data.Position;
import com.example.location.api.data.Signal;
import com.example.location.api.entity.emitter.SignalEmitter;
import com.example.location.internal.entity.emitter.DefaultSignalEmitter;

import org.junit.Test;

import java.util.Optional;

import static com.example.location.IdentifiableObjectMatcher.sameAs;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.IsNot.not;
import static org.mockito.internal.util.JavaEightUtil.emptyOptional;

public class SignalEmitterIntegrationTestCase extends AbstractIntegrationTestCase {

    @Test
    public void getSignalEmitters() throws Exception{
        final String id = "id";
        final String name = "name";
        final Position position = new Position(0,0);
        final String signalAttributeKey = "KEY";
        final String signalAttributeValue = "VALUE";
        final Signal signal = new Signal();
        signal.addAttribute(signalAttributeKey, signalAttributeValue);
        SignalEmitter signalEmitter = new DefaultSignalEmitter(id,name,position,signal);
        registerSignalEmitterInServer(signalEmitter);

        Optional<SignalEmitter> emitterFromServer = getEmitterManager().getSignalEmitter(id);
        assertThat(emitterFromServer, is(not(emptyOptional())));
        assertThat(emitterFromServer.get(), is(sameAs(signalEmitter)));
        assertThat(emitterFromServer.get().getSignal(), is(equalTo(signal)));
    }

}
