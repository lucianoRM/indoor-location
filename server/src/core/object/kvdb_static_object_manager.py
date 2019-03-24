from src.core.database.kv_database import KeyAlreadyExistsException, KeyDoesNotExistException
from src.core.manager.kvdb_backed_manager import KVDBBacked
from src.core.object.static_object_manager import StaticObjectManager, StaticObjectAlreadyExistsException, UnknownStaticObjectException


class KVDBStaticObject(StaticObjectManager, KVDBBacked):
    """StaticObject manager that stores information in a key-value database"""

    __STATIC_OBJECTS_POSITION_KEY = "static_objects"

    def __init__(self, kv_database):
        """
        Constructor for Manager.
        :param kv_database: key-value database to store information about static objects
        """
        super(KVDBStaticObject, self).__init__(kv_database)

    def add_static_object(self, object):
        try:
            return self._database.insert(
                key=self._build_complex_key(self.__STATIC_OBJECTS_POSITION_KEY, object.id),
                value=object
            )
        except KeyAlreadyExistsException:
            raise StaticObjectAlreadyExistsException("Static object with id: " + object.id + " was already registered")

    def get_static_object(self, objectId):
        try:
            return self._database.retrieve(
                key=self._build_complex_key(self.__STATIC_OBJECTS_POSITION_KEY, objectId)
            )
        except KeyDoesNotExistException:
            raise UnknownStaticObjectException("A static object with id: " + objectId + " does not exist")

    def update_static_object(self, objectId, object):
        try:
            return self._database.update(
                key=self._build_complex_key(self.__STATIC_OBJECTS_POSITION_KEY, objectId),
                value=object
            )
        except KeyDoesNotExistException:
            raise UnknownStaticObjectException("A static object with id: " + objectId + " does not exist")

    def remove_static_object(self, objectId):
        try:
            return self._database.remove(
                key=self._build_complex_key(self.__STATIC_OBJECTS_POSITION_KEY, objectId)
            )
        except KeyDoesNotExistException:
            raise UnknownStaticObjectException("Attempting to remove a static object that does not exist. With ID: " + objectId)

    def get_all_static_objects(self):
        try:
            return self._database.retrieve(key=self.__STATIC_OBJECTS_POSITION_KEY).values()
        except KeyDoesNotExistException:
            return []
