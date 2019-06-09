"""
Implementations of abstract classes used for testing
"""
from src.core.anchor.anchor import Anchor
from src.core.emitter.signal_emitter import SignalEmitter
from src.core.object.moving_object import MovingObject
from src.core.object.static_object import StaticObject
from src.core.sensor.sensor import Sensor
from src.core.user.user import User


class FakeStaticSensor(StaticObject, Sensor):
    def __init__(self, id, position, **kwargs):
        super().__init__(id=id, position=position, **kwargs)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

class FakeMovingSensor(MovingObject, Sensor):
    def __init__(self, id, position, **kwargs):
        super().__init__(id=id, position=position, **kwargs)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

class FakeStaticSignalEmitter(StaticObject, SignalEmitter):
    def __init__(self, id, position, **kwargs):
        super().__init__(id=id, position=position, **kwargs)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

class FakeMovingSignalEmitter(MovingObject, SignalEmitter):
    def __init__(self, id, position, **kwargs):
        super().__init__(id=id, position=position, **kwargs)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

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