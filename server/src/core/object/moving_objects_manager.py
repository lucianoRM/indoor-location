

from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, List

from src.core.object.moving_object import MovingObject

T = TypeVar("T", bound=MovingObject)

class MovingObjectsManager:
    """
    API for handling Moving Objects. Moving objects are objects that change their position in the system.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def add_moving_object(self, object_id: str, object: Generic[T]) -> T:
        """
        Add a new moving object
        :param object_id: the unque id to identify the object
        :param object: the object to add
        :raise StaticObjectAlreadyExistsException: if the object was already added
        :return: the object added
        """
        raise NotImplementedError

    @abstractmethod
    def get_moving_object(self, object_id: str) -> T:
        """
        Get an object by id
        :param object_id: the unique id of the moving object to get
        :raise UnknownStaticObjectException: if a moving object with that id does not exist
        :return: the moving object retrieved
        """
        raise NotImplementedError

    @abstractmethod
    def remove_moving_object(self, object_id: str) -> T:
        """
        Remove an moving object by id
        :param object_id: The id to uniquely locate the moving object to remove
        :raise: UnknownStaticObjectException: If the moving object is not found
        :return: The moving object with the given id
        """
        raise NotImplementedError

    @abstractmethod
    def update_moving_object(self, object_id: str, object: Generic[T]) -> T:
        """
        Update an already existent moving object.
        :param object_id: The id of the moving object to be updated
        :param object: The new moving object that will replace the old one with new information
        :raise: UnknownStaticObjectException if no moving object is found with the given id.
        :return: The new moving object updated
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_moving_objects(self) -> List[T]:
        """
        Return all registered moving objects
        :return: all moving objects
        """
        raise NotImplementedError



class MovingObjectsManagerException(Exception):
    """
    Root exception related to an MovingObjectsManager
    """


class MovingObjectAlreadyExistsException(MovingObjectsManagerException):
    """
    Throw this exception when wanting to add an moving object that already exists
    """
    pass


class UnknownMovingObjectException(MovingObjectsManagerException):
    """
    Throw this exception when the requested moving object is not found
    """
    pass