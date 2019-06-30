from abc import ABCMeta, abstractmethod
from typing import TypeVar

from src.core.object.positionable_object import PositionableObject

T = TypeVar('T', bound=PositionableObject)

class PositionableObjectsManager:
    """
    Base abstract manager that handles any type of PositionableObject
    """

    __metaclass = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def get_object(self, object_id: str) -> T:
        """
        Get an object by id
        :param object_id: the unique id for the object
        :raise UnknownObjectException: if the object was never registered
        :return: the object with that id
        """
        raise NotImplementedError

class PositionableObjectsManagerException(Exception):
    pass

class UnknownObjectException(PositionableObjectsManagerException):
    pass