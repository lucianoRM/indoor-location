from abc import ABCMeta, abstractmethod

from src.core.manager.observable_objects_manager import ObservableObjectsManager
from src.core.object.static_objects_manager import StaticObjectsManager


class ObservableStaticObjectsManager(StaticObjectsManager, ObservableObjectsManager):
    """
    Abstract Static objects manager that implements the observable objects interface
    """

    @abstractmethod
    def __init__(self):
        super().__init__()

    __metaclass__ = ABCMeta