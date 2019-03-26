from abc import ABCMeta

from src.core.object.moving_object import MovingObject

class User(MovingObject):
    """
    Abstract class that models an user using the system.
    An user should be any actor of the system that we want to locate.
    """

    __metaclass__ = ABCMeta