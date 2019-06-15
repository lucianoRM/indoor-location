from pytest import raises

from tests.unit.test_implementations.implementations import FakeStaticSignalEmitter, FakeMovingSignalEmitter


class TestSignalEmitter:

    def test_static_signal_emitter_is_immutable(self):
        emitter = FakeStaticSignalEmitter(id = None, position=None, signal=None)
        with raises(AttributeError):
            emitter.signal = None

    def test_moving_signal_emitter_is_immutable(self):
        emitter = FakeMovingSignalEmitter(id=None, position=None, signal=None)
        with raises(AttributeError):
            emitter.signal = None