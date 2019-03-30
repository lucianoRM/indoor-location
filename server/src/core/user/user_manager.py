from abc import ABCMeta, abstractmethod


class UsersManager:
    """
    API for handling Users
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_user(self, user_id, user):
        """
        Add a new user
        :param user_id: the id to store the user
        :param user: the user to add
        :raise UserAlreadyExistsException: if the user was already added
        :return: the user added
        """
        raise NotImplementedError

    @abstractmethod
    def remove_user(self, user_id):
        """
        Remove an user by id
        :param user_id: The id to uniquely locate the user to remove
        :raise: UnkownUserException: If the user is not found
        :return: The user with the given id
        """
        raise NotImplementedError

    @abstractmethod
    def update_user(self, user_id, user):
        """
        Update an already existent user.
        :param user_id: The id of the user to be updated
        :param user: The new user that will replace the old one with new information
        :raise: UnknownUserException if no user is found with the given id.
        :return: The new user updated
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_users(self):
        """
        Return all registered users
        :return: all users
        """
        raise NotImplementedError



class UsersManagerException(Exception):
    """
    Root exception related to an UsersManager
    """


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