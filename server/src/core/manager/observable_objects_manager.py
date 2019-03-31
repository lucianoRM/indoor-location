from abc import ABCMeta, abstractmethod


class ObservableObjectsManager:
    """
    Abstract class that implements the observable pattern. It will call all observers when it modifies data.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        self.__add_object_callbacks = []
        self.__remove_object_callbacks = []

    def call_on_add(self, callback):
        self.__add_object_callbacks.append(callback)

    def call_on_remove(self, callback):
        self.__remove_object_callbacks.append(callback)

    def _on_add(self, object_id: str):
        for callback in self.__add_object_callbacks:
            callback(object_id)

    def _on_remove(self, object_id: str):
        for callback in self.__remove_object_callbacks:
            callback(object_id)