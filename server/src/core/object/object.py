from abc import ABCMeta, abstractmethod

NAME_KEY = "name"

class Object:
    """
    Abstract class to simulate an object part of the system.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, id, **kwargs):
        self._id = id
        self.name = kwargs.get(NAME_KEY, None)

    @property
    def id(self):
        return self._id

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
