

from abc import ABCMeta, abstractmethod


class StaticObjectsManager:
    """
    API for handling Static Objects. Static objects are objects that do not move in the system and generally work as anchors for computing moving object's positions.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_static_object(self,object_id, object):
        """
        Add a new static object
        :param object_id: unique id to identify the object
        :param object: the object to add
        :raise StaticObjectAlreadyExistsException: if the object was already added
        :return: the object added
        """
        raise NotImplementedError

    @abstractmethod
    def get_static_object(self, object_id):
        """
        Get an object by id
        :param object_id: the unique id of the static object to get
        :raise UnknownStaticObjectException: if a static object with that id does not exist
        :return: the static object retrieved
        """
        raise NotImplementedError

    @abstractmethod
    def remove_static_object(self, object_id):
        """
        Remove an static object by id
        :param object_id: The id to uniquely locate the static object to remove
        :raise: UnknownStaticObjectException: If the static object is not found
        :return: The static object with the given id
        """
        raise NotImplementedError

    @abstractmethod
    def update_static_object(self, object_id, object):
        """
        Update an already existent static object.
        :param object_id: The id of the static object to be updated
        :param object: The new static object that will replace the old one with new information
        :raise: UnknownStaticObjectException if no static object is found with the given id.
        :return: The new static object updated
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_static_objects(self):
        """
        Return all registered static objects
        :return: all static objects
        """
        raise NotImplementedError



class StaticObjectsManagerException(Exception):
    """
    Root exception related to an StaticObjectManager
    """


class StaticObjectAlreadyExistsException(StaticObjectsManagerException):
    """
    Throw this exception when wanting to add an static object that already exists
    """
    pass


class UnknownStaticObjectException(StaticObjectsManagerException):
    """
    Throw this exception when the requested static object is not found
    """
    pass