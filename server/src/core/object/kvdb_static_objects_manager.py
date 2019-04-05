from src.core.database.kv_database import KeyAlreadyExistsException, KeyDoesNotExistException
from src.core.manager.kvdb_backed_manager import KVDBBackedManager
from src.core.object.observable_static_objects_manager import ObservableStaticObjectsManager
from src.core.object.static_objects_manager import StaticObjectAlreadyExistsException, UnknownStaticObjectException


class KVDBStaticObjectsManager(KVDBBackedManager, ObservableStaticObjectsManager):
    """StaticObject manager that stores information in a key-value database"""

    __STATIC_OBJECTS_POSITION_KEY = "static_objects"

    def __init__(self, kv_database):
        """
        Constructor for Manager.
        :param kv_database: key-value database to store information about static objects
        """
        super().__init__(kv_database=kv_database)

    def add_static_object(self,object_id, object):
        try:
            value_added = self._database.insert(
                key=self._build_complex_key(self.__STATIC_OBJECTS_POSITION_KEY, object_id),
                value=object
            )
            self._on_add(object_id=object_id)
            return value_added
        except KeyAlreadyExistsException:
            raise StaticObjectAlreadyExistsException("Static object with id: " + object_id + " was already registered")

    def get_static_object(self, object_id):
        try:
            return self._database.retrieve(
                key=self._build_complex_key(self.__STATIC_OBJECTS_POSITION_KEY, object_id)
            )
        except KeyDoesNotExistException:
            raise UnknownStaticObjectException("A static object with id: " + object_id + " does not exist")

    def update_static_object(self, object_id, object):
        try:
            return self._database.update(
                key=self._build_complex_key(self.__STATIC_OBJECTS_POSITION_KEY, object_id),
                value=object
            )
        except KeyDoesNotExistException:
            raise UnknownStaticObjectException("A static object with id: " + object_id + " does not exist")

    def remove_static_object(self, object_id):
        try:
            object_removed = self._database.remove(
                key=self._build_complex_key(self.__STATIC_OBJECTS_POSITION_KEY, object_id)
            )
            self._on_remove(object_id=object_id)
            return object_removed
        except KeyDoesNotExistException:
            raise UnknownStaticObjectException("Attempting to remove a static object that does not exist. With ID: " + object_id)

    def get_all_static_objects(self):
        try:
            return self._database.retrieve(key=self.__STATIC_OBJECTS_POSITION_KEY).values()
        except KeyDoesNotExistException:
            return []
