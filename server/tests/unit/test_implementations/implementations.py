"""
Implementations of abstract classes used for testing
"""
from src.core.anchor.anchor import Anchor
from src.core.object.moving_object import MovingObject
from src.core.object.static_object import StaticObject
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