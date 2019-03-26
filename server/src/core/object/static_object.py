from abc import ABCMeta

from src.core.object.positionable_object import PositionableObject


class StaticObject(PositionableObject):
    """
    Abstract class to model a PositionableObject that does not modify it's position in the system
    """

    __metaclass__ = ABCMeta

