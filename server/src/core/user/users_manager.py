from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, List

from src.core.user.user import User

T = TypeVar("T", bound=User)

class UsersManager:
    """
    API for handling Users
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def add_user(self, user_id: str, user: Generic[T]) -> T:
        """
        Add a new user
        :param user_id: the id to store the user
        :param user: the user to add
        :raise UserAlreadyExistsException: if the user was already added
        :return: the user added
        """
        raise NotImplementedError

    @abstractmethod
    def get_user(self, user_id: str) -> T:
        """
        Get user by id
        :param user_id: the id of the user to get
        :return: The user with id: user_id
        :raise UnknownUserException: If the user does not exist
        """
        raise NotImplementedError

    @abstractmethod
    def remove_user(self, user_id: str) -> T:
        """
        Remove an user by id
        :param user_id: The id to uniquely locate the user to remove
        :raise: UnkownUserException: If the user is not found
        :return: The user with the given id
        """
        raise NotImplementedError

    @abstractmethod
    def update_user(self, user_id:str, user: Generic[T]) -> T:
        """
        Update an already existent user.
        :param user_id: The id of the user to be updated
        :param user: The new user that will replace the old one with new information
        :raise: UnknownUserException if no user is found with the given id.
        :return: The new user updated
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_users(self) -> List[T]:
        """
        Return all registered users
        :return: all users
        """
        raise NotImplementedError



class UsersManagerException(Exception):
    """
    Root exception related to an UsersManager
    """
    pass


class UserAlreadyExistsException(UsersManagerException):
    """
    Throw this exception when wanting to add an user that already exists
    """
    pass


class UnknownUserException(UsersManagerException):
    """
    Throw this exception when the requested user is not found
    """
    pass