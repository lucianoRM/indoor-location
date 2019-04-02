from typing import Generic, List

from src.core.manager.positionable_objects_manager import PositionableObjectsManager, T, ObjectAlreadyExistsException, \
    UnknownObjectException
from src.core.object.moving_object import MovingObject
from src.core.object.moving_objects_manager import UnknownMovingObjectException, MovingObjectAlreadyExistsException
from src.core.object.observable_moving_objects_manager import ObservableMovingObjectsManager
from src.core.object.observable_static_objects_manager import ObservableStaticObjectsManager
from src.core.object.static_object import StaticObject
from src.core.object.static_objects_manager import UnknownStaticObjectException, StaticObjectAlreadyExistsException

class ObserverComposedObjectsManager(PositionableObjectsManager):
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
        self.__static_objects_manager.call_on_add(lambda object_id : self.__static_objects.add(object_id))
        self.__static_objects_manager.call_on_remove(lambda object_id : self.__static_objects.remove(object_id))

        self.__moving_objects_manager = observable_moving_objects_manager
        self.__moving_objects_manager.call_on_add(lambda object_id: self.__moving_objects.add(object_id))
        self.__moving_objects_manager.call_on_remove(lambda object_id: self.__moving_objects.remove(object_id))

    def add_object(self, object_id: str, object: Generic[T]) -> T:
        try:
            if isinstance(object, StaticObject):
                return self.__static_objects_manager.add_static_object(object_id=object_id,
                                                                       object=object)
            elif isinstance(object, MovingObject):
                return self.__moving_objects_manager.add_moving_object(object_id=object_id,
                                                                       object=object)
        except (StaticObjectAlreadyExistsException, MovingObjectAlreadyExistsException):
            raise ObjectAlreadyExistsException()

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

    def update_object(self, object_id: str, object: Generic[T]) -> T:
        try:
            if object_id in self.__moving_objects:
                return self.__moving_objects_manager.update_moving_object(object_id=object_id, object=object)
            elif object_id in self.__static_objects:
                return self.__static_objects_manager.update_static_object(object_id=object_id, object=object)
        except UnknownStaticObjectException:
            self.__static_objects.remove(object_id)
        except UnknownMovingObjectException:
            self.__moving_objects.remove(object_id)
        raise UnknownObjectException()

    def remove_object(self, object_id: str) -> T:
        try:
            if object_id in self.__moving_objects:
                return self.__moving_objects_manager.remove_moving_object(object_id=object_id)
            elif object_id in self.__static_objects:
                return self.__static_objects_manager.remove_static_object(object_id=object_id)
        except UnknownStaticObjectException:
            self.__static_objects.remove(object_id)
        except UnknownMovingObjectException:
            self.__moving_objects.remove(object_id)
        raise UnknownObjectException()

    def get_all_objects(self) -> List[T]:
        all_objects = []
        for id in self.__moving_objects:
            all_objects.append(self.__moving_objects_manager.get_moving_object(object_id=id))
        for id in self.__static_objects:
            all_objects.append(self.__static_objects_manager.get_static_object(object_id=id))
        return all_objects
