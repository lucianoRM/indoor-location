from abc import ABCMeta, abstractmethod
from typing import List, TypeVar, Generic

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
    def add_object(self, object_id: str, object: Generic[T]) -> T:
        """
        Add a new object
        :param object_id: the unique id for the object
        :param object: the object to be added
        :raise ObjectAlreadyExistsException: If the id was already registered
        :return: the object added
        """
        raise NotImplementedError

    @abstractmethod
    def get_object(self, object_id: str) -> T:
        """
        Get an object by id
        :param object_id: the unique id for the object
        :raise UnknownObjectException: if the object was never registered
        :return: the object with that id
        """
        raise NotImplementedError

    @abstractmethod
    def update_object(self, object_id: str, object: Generic[T]) -> T:
        """
        Update data of object with id: object_id
        :param object_id: the id for the object
        :param object: the new object to update
        :raise UnknownObjectException: If the id was never registered
        :return: the updated object
        """
        raise NotImplementedError

    @abstractmethod
    def remove_object(self, object_id: str) -> T:
        """
        Remove object by id
        :param object_id: the id for the object to remove
        :raise UnknownObjectException: If the id was never registered
        :return: The removed object
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_objects(self) -> List[T]:
        """
        :return: All registered objects
        """

class PositionableObjectsManagerException(Exception):
    pass

class UnknownObjectException(PositionableObjectsManagerException):
    pass

class ObjectAlreadyExistsException(PositionableObjectsManagerException):
    pass