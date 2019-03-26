from abc import ABCMeta

from src.core.object.positionable_object import PositionableObject


class MovingObject(PositionableObject):
    """
    Abstract class to model an object that changes it's position in the system
    """
    __metaclass__ = ABCMeta

    @PositionableObject.position.setter
    def position(self, position):
        self._position = position