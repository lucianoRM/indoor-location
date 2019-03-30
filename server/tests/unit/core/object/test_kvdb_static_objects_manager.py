from pytest import fixture, raises

from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.object.kvdb_static_objects_manager import KVDBStaticObjectsManager
from src.core.object.static_objects_manager import StaticObjectAlreadyExistsException, UnknownStaticObjectException
from tests.unit.test_implementations.implementations import TestStaticObject


class TestKVDBStaticObjectsManager:

    __STATIC_OBJECT_ID = "object_id"

    @fixture(autouse=True)
    def setUp(self):
        self.__test_static_object = TestStaticObject(
                                        id=self.__STATIC_OBJECT_ID,
                                        position=(0,0),
                                        name="static_objectName")
        self.__static_object_manager = KVDBStaticObjectsManager(MemoryKVDatabase())

    def test_add_static_object(self):
        self.__static_object_manager.add_static_object(object_id=self.__STATIC_OBJECT_ID, object=self.__test_static_object)
        assert self.__static_object_manager.get_static_object(object_id=self.__STATIC_OBJECT_ID) == self.__test_static_object

    def test_add_static_object_with_same_id(self):
        self.__static_object_manager.add_static_object(object_id=self.__STATIC_OBJECT_ID, object=self.__test_static_object)
        sameIdStaticObject = TestStaticObject(id=self.__STATIC_OBJECT_ID,
                                          position=(1,1),
                                          name="otherStaticObject")
        with raises(StaticObjectAlreadyExistsException):
            self.__static_object_manager.add_static_object(object_id=self.__STATIC_OBJECT_ID, object=sameIdStaticObject)

    def test_add_multiple_static_objects_and_get_all(self):
        all_static_objects = [TestStaticObject(id=str(static_object_id), name="objectName", position= (0,0)) for static_object_id in range(100)]
        for static_object in all_static_objects:
            self.__static_object_manager.add_static_object(object_id=static_object.id, object=static_object)
        retrieved_static_objects = self.__static_object_manager.get_all_static_objects()
        for static_object in all_static_objects:
            assert static_object in retrieved_static_objects

    def test_remove_static_object_and_try_get_it(self):
        self.__static_object_manager.add_static_object(object_id=self.__STATIC_OBJECT_ID, object=self.__test_static_object)
        assert self.__static_object_manager.get_static_object(object_id=self.__STATIC_OBJECT_ID) == self.__test_static_object
        self.__static_object_manager.remove_static_object(self.__STATIC_OBJECT_ID)
        with raises(UnknownStaticObjectException):
            self.__static_object_manager.get_static_object(object_id=self.__STATIC_OBJECT_ID)

    def test_get_static_object_from_empty_db(self):
        with raises(UnknownStaticObjectException):
            self.__static_object_manager.get_static_object(object_id=self.__STATIC_OBJECT_ID)

    def test_update_static_object(self):
        self.__static_object_manager.add_static_object(object_id=self.__STATIC_OBJECT_ID, object=self.__test_static_object)
        newStaticObject = TestStaticObject(id=self.__STATIC_OBJECT_ID,
                                       name= "newStaticObjectName",
                                       position= (1,1))
        self.__static_object_manager.update_static_object(self.__STATIC_OBJECT_ID, newStaticObject)
        assert self.__static_object_manager.get_static_object(object_id=self.__STATIC_OBJECT_ID) == newStaticObject

    def test_update_not_existent_static_object(self):
        with raises(UnknownStaticObjectException):
            self.__static_object_manager.update_static_object(object_id="missingStaticObjectId", object={})
