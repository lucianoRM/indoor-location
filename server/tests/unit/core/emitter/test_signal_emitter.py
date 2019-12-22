from pytest import raises

from src.core.emitter.signal_emitter import SignalEmitter


class TestSignalEmitter:

    def test_signal_emitter_signal_is_immutable(self):
        emitter = SignalEmitter(id = None, signal=None, position=None)
        with raises(AttributeError):
            emitter.signal = None