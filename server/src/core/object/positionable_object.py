from abc import ABCMeta, abstractmethod

from src.core.object.object import Object


class PositionableObject(Object):
    """
    Abstract class to model an object that can be located within the system
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, id, position, **kwargs):
        super(PositionableObject, self).__init__(id, **kwargs)
        self._position = position

    @property
    def position(self):
        return self._position