from abc import ABCMeta, abstractmethod

from src.core.object.static_object import StaticObject

class Anchor(StaticObject):
    """
    Abstract class to model anchors in the system. Anchors are static objects that don't modify its position.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)