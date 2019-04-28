from abc import ABCMeta, abstractmethod

from src.core.manager.observable_objects_manager import ObservableObjectsManager
from src.core.object.moving_objects_manager import MovingObjectsManager

class ObservableMovingObjectsManager(MovingObjectsManager, ObservableObjectsManager):
    """
    Abstract class to define a moving objects manager that implements the observable objects manager interface
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
