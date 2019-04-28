from abc import ABCMeta, abstractmethod
from typing import Callable

from src.core.object.object import Object


class ObservableObjectsManager:
    """
    Abstract class that implements the observable pattern. It will call all observers when it modifies data.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        self.__add_object_callbacks = []
        self.__remove_object_callbacks = []
        super().__init__(**kwargs)

    def call_on_add(self, callback: Callable):
        self.__add_object_callbacks.append(callback)

    def call_on_remove(self, callback: Callable):
        self.__remove_object_callbacks.append(callback)

    def _on_add(self, object_id: str, object: Object):
        for callback in self.__add_object_callbacks:
            callback(object_id, object)

    def _on_remove(self, object_id: str, object: Object):
        for callback in self.__remove_object_callbacks:
            callback(object_id, object)