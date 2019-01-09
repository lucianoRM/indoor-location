from abc import ABCMeta, abstractmethod


class Database:
    """
    API for defining Database implementations. Note that the DB does not handle logic for sea
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def insert(self, key, value, **kwargs):
        """
        Insert a new value reached by the provided key.
        :param key: key that defines where to add the new value.
        It can be composed by multiple keys. It's up to the implementation to know how to interpret the key
        :param value: New value to add
        :raise ValueAlreadyExistsException if the key is already in use.
        :return added value
        """
        raise NotImplementedError

    @abstractmethod
    def upsert(self, key, value, **kwargs):
        """
        Insert a new value reached by the provided key. If the value with that key already exists, replace it.
        :param key: key that defines where to add the new value.
        :param value: New value to add
        :return added value
        """
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, key, **kwargs):
        """
        Get the value that relates to the key
        :param key: the key to find the value
        :raise KeyDoesNotExistException if the key is not in the db.
        :return: The value related to that key
        """
        raise NotImplementedError

    @abstractmethod
    def remove(self, key, **kwargs):
        """
        Remove value and key from DB.
        :param key: key for value to be removed
        :return: removed value
        :raise KeyDoesNotExistException if the key is not in the DB
        """
        raise NotImplementedError


class DatabaseException(Exception):
    """
    Exception related to any DB related issue.
    """
    pass


class KeyAlreadyExistsException(DatabaseException):
    """
    Throw this exception if wanting to add a new value and the key is already used
    """
    pass


class KeyDoesNotExistException(DatabaseException):
    """
    Throw this exception if the key does not exist in the DB
    """
    pass
