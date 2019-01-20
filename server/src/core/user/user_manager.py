from abc import ABCMeta, abstractmethod


class UserManager:
    """
    API for handling Users
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_user(self, user):
        """
        Add a new user
        :param user: the user to add
        :raise UserAlreadyExistsException: if the user was already added
        :return: the user added
        """
        raise NotImplementedError

    @abstractmethod
    def remove_user(self, userId):
        """
        Remove an user by id
        :param userId: The id to uniquely locate the user to remove
        :raise: UnkownUserException: If the user is not found
        :return: The user with the given id
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_users(self):
        """
        Return all registered users
        :return: all users
        """
        raise NotImplementedError



class UserManagerException(Exception):
    """
    Root exception related to an UserManager
    """


class UserAlreadyExistsException(UserManagerException):
    """
    Throw this exception when wanting to add an user that already exists
    """
    pass


class UnknownUserException(UserManagerException):
    """
    Throw this exception when the requested user is not found
    """
    pass