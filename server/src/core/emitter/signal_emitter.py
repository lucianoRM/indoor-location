from abc import ABCMeta, abstractmethod


class SignalEmitter:
    """
    Abstract class that models an object that emits a signal
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def __init__(self, id: str, **kwargs):
        self._id = id
        self.name = kwargs.pop(NAME_KEY, None)
        super().__init__(**kwargs)

    @property
    def id(self):
        return self._id

    def __eq__(self, other: 'Object'):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other: 'Object'):
        return not self.__eq__(other)