from abc import ABCMeta, abstractmethod

from src.core.object.moving_object import MovingObject

class User(MovingObject):
    """
    Abstract class that models an user using the system.
    An user should be any actor of the system that we want to locate.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)