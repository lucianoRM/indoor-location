from typing import TypeVar, Generic, List

from src.core.database.kv_database import KeyAlreadyExistsException, KeyDoesNotExistException, KVDatabase
from src.core.manager.kvdb_backed_manager import KVDBBackedManager
from src.core.object.observable_static_objects_manager import ObservableStaticObjectsManager
from src.core.object.static_object import StaticObject
from src.core.object.static_objects_manager import StaticObjectAlreadyExistsException, UnknownStaticObjectException

T = TypeVar("T", bound=StaticObject)

class KVDBStaticObjectsManager(KVDBBackedManager, ObservableStaticObjectsManager):
    """StaticObject manager that stores information in a key-value database"""

    __STATIC_OBJECTS_POSITION_KEY = "static_objects"

    def __init__(self, kv_database: KVDatabase):
        """
        Constructor for Manager.
        :param kv_database: key-value database to store information about static objects
        """
        super().__init__(kv_database=kv_database)

    def add_static_object(self,object_id: str, object: Generic[T]) -> T:
        try:
            value_added = self._database.insert(
                key=self._build_complex_key(self.__STATIC_OBJECTS_POSITION_KEY, object_id),
                value=object
            )
            self._on_add(object_id=object_id, object=value_added)
            return value_added
        except KeyAlreadyExistsException:
            raise StaticObjectAlreadyExistsException("Static object with id: " + object_id + " was already registered")

    def get_static_object(self, object_id: str) -> T:
        try:
            return self._database.retrieve(
                key=self._build_complex_key(self.__STATIC_OBJECTS_POSITION_KEY, object_id)
            )
        except KeyDoesNotExistException:
            raise UnknownStaticObjectException("A static object with id: " + object_id + " does not exist")

    def update_static_object(self, object_id: str, object: Generic[T]) -> T:
        try:
            return self._database.update(
                key=self._build_complex_key(self.__STATIC_OBJECTS_POSITION_KEY, object_id),
                value=object
            )
        except KeyDoesNotExistException:
            raise UnknownStaticObjectException("A static object with id: " + object_id + " does not exist")

    def remove_static_object(self, object_id: str) -> T:
        try:
            object_removed = self._database.remove(
                key=self._build_complex_key(self.__STATIC_OBJECTS_POSITION_KEY, object_id)
            )
            self._on_remove(object_id=object_id, object=object_removed)
            return object_removed
        except KeyDoesNotExistException:
            raise UnknownStaticObjectException("Attempting to remove a static object that does not exist. With ID: " + object_id)

    def get_all_static_objects(self) -> List[T]:
        try:
            return self._database.retrieve(key=self.__STATIC_OBJECTS_POSITION_KEY).values()
        except KeyDoesNotExistException:
            return []
