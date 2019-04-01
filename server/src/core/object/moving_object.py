from abc import ABCMeta, abstractmethod

from src.core.object.positionable_object import PositionableObject


class MovingObject(PositionableObject):
    """
    Abstract class to model an object that changes it's position in the system
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @PositionableObject.position.setter
    def position(self, position):
        self._position = position