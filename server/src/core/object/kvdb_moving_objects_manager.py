from typing import Generic, List

from src.core.database.kv_database import KeyAlreadyExistsException, KeyDoesNotExistException
from src.core.manager.kvdb_backed_manager import KVDBBackedManager
from src.core.object.moving_objects_manager import MovingObjectAlreadyExistsException, UnknownMovingObjectException, T
from src.core.object.observable_moving_objects_manager import ObservableMovingObjectsManager

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

    def add_moving_object(self,object_id: str, object: Generic[T]) -> T:
        try:
            object_added = self._database.insert(
                key=self._build_complex_key(self.__MOVING_OBJECTS_POSITION_KEY, object_id),
                value=object
            )
            self._on_add(object_id=object_id)
            return object_added
        except KeyAlreadyExistsException:
            raise MovingObjectAlreadyExistsException("Moving object with id: " + object_id + " was already registered")

    def get_moving_object(self, object_id: str) -> T:
        try:
            return self._database.retrieve(
                key=self._build_complex_key(self.__MOVING_OBJECTS_POSITION_KEY, object_id)
            )
        except KeyDoesNotExistException:
            raise UnknownMovingObjectException("A moving object with id: " + object_id + " does not exist")

    def update_moving_object(self, object_id: str, object: Generic[T]) -> T:
        try:
            return self._database.update(
                key=self._build_complex_key(self.__MOVING_OBJECTS_POSITION_KEY, object_id),
                value=object
            )
        except KeyDoesNotExistException:
            raise UnknownMovingObjectException("A moving object with id: " + object_id + " does not exist")

    def remove_moving_object(self, object_id: str) -> T:
        try:
            removed_object = self._database.remove(
                key=self._build_complex_key(self.__MOVING_OBJECTS_POSITION_KEY, object_id)
            )
            self._on_remove(object_id=object_id)
            return removed_object
        except KeyDoesNotExistException:
            raise UnknownMovingObjectException("Attempting to remove a moving object that does not exist. With ID: " + object_id)

    def get_all_moving_objects(self) -> List[T]:
        try:
            return self._database.retrieve(key=self.__MOVING_OBJECTS_POSITION_KEY).values()
        except KeyDoesNotExistException:
            return []
