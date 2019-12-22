from src.core.manager.observable_objects_manager import Callback
from src.core.manager.positionable_objects_manager import PositionableObjectsManager, T, UnknownObjectException
from src.core.object.moving_objects_manager import UnknownMovingObjectException
from src.core.object.observable_moving_objects_manager import ObservableMovingObjectsManager
from src.core.object.observable_static_objects_manager import ObservableStaticObjectsManager
from src.core.object.static_objects_manager import UnknownStaticObjectException


class PositionableObjectsManagerObserver(PositionableObjectsManager):
    """
    Class that represents an observer objects manager that listens to multiple ObservableObjectsManagers.
    """

    def __init__(self,
                 observable_static_objects_manager: ObservableStaticObjectsManager,
                 observable_moving_objects_manager: ObservableMovingObjectsManager):

        super().__init__()
        self.__static_objects = set()
        self.__moving_objects = set()

        self.__static_objects_manager = observable_static_objects_manager
        self.__static_objects_manager.call_on_add(Callback(self.__add_static_object, self.__remove_static_object))
        self.__static_objects_manager.call_on_remove(Callback(self.__remove_static_object, self.__add_static_object))

        self.__moving_objects_manager = observable_moving_objects_manager
        self.__moving_objects_manager.call_on_add(Callback(self.__add_moving_object, self.__remove_moving_object))
        self.__moving_objects_manager.call_on_remove(Callback(self.__remove_moving_object, self.__add_moving_object))

        self.accepted_types = []

    def __add_static_object(self, obj_id: str, *args):
        self.__static_objects.add(obj_id)

    def __add_moving_object(self, obj_id: str, *args):
        self.__moving_objects.add(obj_id)

    def __remove_static_object(self, obj_id: str, *args):
        self.__static_objects.remove(obj_id)

    def __remove_moving_object(self, obj_id: str, *args):
        self.__moving_objects.remove(obj_id)

    def register_on_add_callback(self, callback: Callback):
        self.__static_objects_manager.call_on_add(callback)
        self.__moving_objects_manager.call_on_add(callback)

    def register_on_remove_callback(self, callback: Callback):
        self.__static_objects_manager.call_on_remove(callback)
        self.__moving_objects_manager.call_on_remove(callback)

    def register_on_update_callback(self, callback: Callback):
        self.__static_objects_manager.call_on_update(callback)
        self.__moving_objects_manager.call_on_update(callback)

    def get_object(self, object_id: str) -> T:
        try:
            if object_id in self.__moving_objects:
                return self.__moving_objects_manager.get_moving_object(object_id=object_id)
            elif object_id in self.__static_objects:
                return self.__static_objects_manager.get_static_object(object_id=object_id)
        except UnknownStaticObjectException:
            self.__static_objects.remove(object_id)
        except UnknownMovingObjectException:
            self.__moving_objects.remove(object_id)
        raise UnknownObjectException()
