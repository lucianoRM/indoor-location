from abc import ABCMeta, abstractmethod

from src.core.object.positionable_object import PositionableObject


class StaticObject(PositionableObject):
    """
    Abstract class to model a PositionableObject that does not modify it's position in the system
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

