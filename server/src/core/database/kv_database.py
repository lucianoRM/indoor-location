from abc import ABCMeta, abstractmethod


class KVDatabase:
    """
    API for defining key-value Database implementations.
    DB should be able to handle complex keys using a Key delimiter.
    For example, with "." as the delimiter:

    insert("a.b.c", "ABC")
    insert("a.b.d", "ABD")
    retrieve("a.b") should return: {"c": "ABC" , "d" : "ABD"}
    """
    __metaclass__ = ABCMeta

    __KEYS_DELIMITER = "."

    @abstractmethod
    def insert(self, key, value, **kwargs):
        """
        Insert a new value reached by the provided key.
        :param key: key that defines where to add the new value.
        It can be composed by multiple keys. It's up to the implementation to know how to interpret the key
        :param value: New value to add
        :raise KeyAlreadyExistsException if the key is already in use.
        :return added value
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, key, value, **kwargs):
        """
        Update a value from the DB. If the value does not exist, fail with KeyDoesNotExistsException.
        :param key: The key of the value to update
        :param value: The new value that will replace the old one in the DB
        :raise KeyDoesNotExistsException: if the key is not found in the DB.
        :return: The new value updated in the DB
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

    def get_keys_delimiter(self):
        """
        :return: Keys delimiter used to build complex keys
        """
        return self.__KEYS_DELIMITER


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
