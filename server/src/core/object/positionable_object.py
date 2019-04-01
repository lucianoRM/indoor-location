from abc import ABCMeta, abstractmethod

from src.core.object.object import Object


class PositionableObject(Object):
    """
    Abstract class to model an object that can be located within the system
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, id, position, **kwargs):
        self._position = position
        super().__init__(id=id, **kwargs)

    @property
    def position(self):
        return self._position