"""
Implementations of abstract classes used for testing
"""
from src.core.anchor.anchor import Anchor
from src.core.emitter.signal_emitter import SignalEmitter
from src.core.object.moving_object import MovingObject
from src.core.object.static_object import StaticObject
from src.core.sensor.sensor import Sensor
from src.core.user.user import User


class TestStaticSensor(StaticObject, Sensor):
    def __init__(self, id, position, **kwargs):
        super().__init__(id, position, **kwargs)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

class TestMovingSensor(MovingObject, Sensor):
    def __init__(self, id, position, **kwargs):
        super().__init__(id, position, **kwargs)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

class TestStaticSignalEmitter(StaticObject, SignalEmitter):
    def __init__(self, id, position, **kwargs):
        super().__init__(id, position, **kwargs)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

class TestMovingSignalEmitter(MovingObject, SignalEmitter):
    def __init__(self, id, position, **kwargs):
        super().__init__(id, position, **kwargs)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

class TestAnchor(Anchor):
    def __init__(self, id, position, **kwargs):
        super().__init__(id, position, **kwargs)

class TestStaticObject(StaticObject):
    def __init__(self, id, position, **kwargs):
        super(TestStaticObject, self).__init__(id, position, **kwargs)

class TestMovingObject(MovingObject):
    def __init__(self, id, position, **kwargs):
        super(TestMovingObject, self).__init__(id, position, **kwargs)

class TestUser(User):
    def __init__(self, id, position, **kwargs):
        super(TestUser, self).__init__(id, position, **kwargs)