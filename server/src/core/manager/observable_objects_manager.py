from abc import ABCMeta, abstractmethod
from typing import List

from src.core.object.object import Object


class Callback:

    def __init__(self, callback: callable, error_handler: callable):
        self.__callback = callback
        self.__error_handler = error_handler

    def exec(self, *args, **kwargs):
        return self.__callback(*args, **kwargs)

    def rollback(self, *args, **kwargs):
        return self.__error_handler(*args, **kwargs)


class ObservableObjectsManager:
    """
    Abstract class that implements the observable pattern. It will call all observers when it modifies data.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        self.__add_object_callbacks = []
        self.__remove_object_callbacks = []
        self.__update_object_callbacks = []
        super().__init__(**kwargs)

    def call_on_add(self, callback: Callback):
        self.__add_object_callbacks.append(callback)

    def call_on_remove(self, callback: Callback):
        self.__remove_object_callbacks.append(callback)

    def call_on_update(self, callback: Callback):
        self.__update_object_callbacks.append(callback)

    def _on_add(self, object_id: str, object: Object):
        self.__execute_transactionally(self.__add_object_callbacks, object_id, object)

    def _on_remove(self, object_id: str, object: Object):
        self.__execute_transactionally(self.__remove_object_callbacks, object_id, object)

    def _on_update(self, object_id: str, new_obj: Object, old_obj: Object):
        self.__execute_transactionally(self.__update_object_callbacks, object_id, new_obj, old_obj)

    def __execute_transactionally(self,callbacks: List[Callback], *args, **kwargs):
        executed = []
        try:
            for callback in callbacks:
                callback.exec(*args, **kwargs)
                executed.append(callback)
        except Exception as e:
            for callback in executed:
                callback.rollback(*args, **kwargs)
                raise e
