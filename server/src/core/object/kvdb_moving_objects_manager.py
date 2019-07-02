from typing import Generic, List, TypeVar

from src.core.database.kv_database import KeyAlreadyExistsException, KeyDoesNotExistException
from src.core.manager.kvdb_backed_manager import KVDBBackedManager
from src.core.object.moving_object import MovingObject
from src.core.object.moving_objects_manager import MovingObjectAlreadyExistsException, UnknownMovingObjectException
from src.core.object.observable_moving_objects_manager import ObservableMovingObjectsManager

T = TypeVar("T", bound=MovingObject)


class KVDBMovingObjectsManager(KVDBBackedManager, ObservableMovingObjectsManager):
    """MovingObjects manager that stores information in a key-value database"""

    __MOVING_OBJECTS_POSITION_KEY = "moving_objects"

    def __init__(self, kv_database):
        """
        Constructor for Manager.
        :param kv_database: key-value database to store information about moving objects
        """
        KVDBBackedManager.__init__(self, kv_database=kv_database)
        ObservableMovingObjectsManager.__init__(self)

    def add_moving_object(self, object_id: str, object: Generic[T]) -> T:
        key = self._build_complex_key(self.__MOVING_OBJECTS_POSITION_KEY, object_id)
        try:
            object_added = self._database.insert(
                key=key,
                value=object
            )
        except KeyAlreadyExistsException:
            raise MovingObjectAlreadyExistsException("Moving object with id: " + object_id + " was already registered")

        # update listeners
        try:
            self._on_add(object_id=object_id, object=object_added)
            return object_added
        except Exception as e:
            # rollback
            self._database.remove(key=key)
            raise e

    def get_moving_object(self, object_id: str) -> T:
        try:
            return self._database.retrieve(
                key=self._build_complex_key(self.__MOVING_OBJECTS_POSITION_KEY, object_id)
            )
        except KeyDoesNotExistException:
            raise UnknownMovingObjectException("A moving object with id: " + object_id + " does not exist")

    def update_moving_object(self, object_id: str, object: Generic[T]) -> T:
        key = self._build_complex_key(self.__MOVING_OBJECTS_POSITION_KEY, object_id)
        try:
            old_obj = self._database.retrieve(key=key)
            object_udpated = self._database.update(
                key=key,
                value=object
            )
        except KeyDoesNotExistException:
            raise UnknownMovingObjectException("A moving object with id: " + object_id + " does not exist")

        # update listeners
        try:
            self._on_update(object_id=object_id, old_obj=old_obj, new_obj=object_udpated)
            return object_udpated
        except Exception as e:
            # rollback
            self._database.update(key=key, value=old_obj)
            raise e

    def remove_moving_object(self, object_id: str) -> T:
        key = self._build_complex_key(self.__MOVING_OBJECTS_POSITION_KEY, object_id)
        try:
            removed_object = self._database.remove(
                key=key,
            )
        except KeyDoesNotExistException:
            raise UnknownMovingObjectException(
                "Attempting to remove a moving object that does not exist. With ID: " + object_id)

        # update listeners
        try:
            self._on_remove(object_id=object_id, object=removed_object)
            return removed_object
        except Exception as e:
            # rollback
            self._database.insert(key=key, value=removed_object)
            raise e

    def get_all_moving_objects(self) -> List[T]:
        try:
            return list(self._database.retrieve(key=self.__MOVING_OBJECTS_POSITION_KEY).values())
        except KeyDoesNotExistException:
            return []
