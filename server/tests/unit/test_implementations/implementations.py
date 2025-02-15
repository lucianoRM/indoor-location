"""
Implementations of abstract classes used for testing
"""
from src.core.anchor.anchor import Anchor
from src.core.emitter.signal_emitter import SignalEmitter
from src.core.object.moving_object import MovingObject
from src.core.object.static_object import StaticObject
from src.core.sensor.sensor import Sensor
from src.core.user.user import User

class FakeAnchor(Anchor):
    def __init__(self, id, position, **kwargs):
        super().__init__(id=id, position=position, **kwargs)

class FakeStaticObject(StaticObject):
    def __init__(self, id, position, **kwargs):
        super().__init__(id=id, position=position, **kwargs)

class FakeMovingObject(MovingObject):
    def __init__(self, id, position, **kwargs):
        super().__init__(id=id, position=position, **kwargs)

class FakeUser(User):
    def __init__(self, id, position, **kwargs):
        super().__init__(id=id, position=position, **kwargs)

class FakeSensor(Sensor):
    def __init__(self, id, position=None, **kwargs):
        super().__init__(id=id, position=position, **kwargs)

class FakeSignalEmitter(SignalEmitter):
    def __init__(self, id, signal=None, position=None, **kwargs):
        super().__init__(id=id, signal=signal, position=position, **kwargs)