from pytest import fixture, raises

from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.manager.observable_objects_manager import Callback
from src.core.object.kvdb_moving_objects_manager import KVDBMovingObjectsManager
from src.core.object.moving_objects_manager import MovingObjectAlreadyExistsException, UnknownMovingObjectException
from tests.unit.test_implementations.implementations import FakeMovingObject


class TestKVDBMovingObjectsManager:
    __MOVING_OBJECT_ID = "object_id"

    @fixture(autouse=True)
    def setUp(self):
        self.__test_moving_object = FakeMovingObject(
            id=self.__MOVING_OBJECT_ID,
            position=(0, 0),
            name="moving_objectName")
        self.__moving_object_manager = KVDBMovingObjectsManager(MemoryKVDatabase())

    def test_add_moving_object(self):
        self.__moving_object_manager.add_moving_object(object_id=self.__MOVING_OBJECT_ID,
                                                       object=self.__test_moving_object)
        assert self.__moving_object_manager.get_moving_object(
            object_id=self.__MOVING_OBJECT_ID) == self.__test_moving_object

    def test_add_moving_object_with_same_id(self):
        self.__moving_object_manager.add_moving_object(object_id=self.__MOVING_OBJECT_ID,
                                                       object=self.__test_moving_object)
        sameIdMovingObject = FakeMovingObject(id=self.__MOVING_OBJECT_ID,
                                              position=(1, 1),
                                              name="otherMovingObject")
        with raises(MovingObjectAlreadyExistsException):
            self.__moving_object_manager.add_moving_object(object_id=self.__MOVING_OBJECT_ID, object=sameIdMovingObject)

    def test_add_multiple_moving_objects_and_get_all(self):
        all_moving_objects = [FakeMovingObject(id=str(moving_object_id), name="objectName", position=(0, 0)) for
                              moving_object_id in range(100)]
        for moving_object in all_moving_objects:
            self.__moving_object_manager.add_moving_object(object_id=moving_object.id, object=moving_object)
        retrieved_moving_objects = self.__moving_object_manager.get_all_moving_objects()
        for moving_object in all_moving_objects:
            assert moving_object in retrieved_moving_objects

    def test_remove_moving_object_and_try_get_it(self):
        self.__moving_object_manager.add_moving_object(object_id=self.__MOVING_OBJECT_ID,
                                                       object=self.__test_moving_object)
        assert self.__moving_object_manager.get_moving_object(
            object_id=self.__MOVING_OBJECT_ID) == self.__test_moving_object
        self.__moving_object_manager.remove_moving_object(self.__MOVING_OBJECT_ID)
        with raises(UnknownMovingObjectException):
            self.__moving_object_manager.get_moving_object(object_id=self.__MOVING_OBJECT_ID)

    def test_get_moving_object_from_empty_db(self):
        with raises(UnknownMovingObjectException):
            self.__moving_object_manager.get_moving_object(object_id=self.__MOVING_OBJECT_ID)

    def test_update_moving_object(self):
        self.__moving_object_manager.add_moving_object(object_id=self.__MOVING_OBJECT_ID,
                                                       object=self.__test_moving_object)
        newMovingObject = FakeMovingObject(id=self.__MOVING_OBJECT_ID,
                                           name="newMovingObjectName",
                                           position=(1, 1))
        self.__moving_object_manager.update_moving_object(self.__MOVING_OBJECT_ID, newMovingObject)
        assert self.__moving_object_manager.get_moving_object(object_id=self.__MOVING_OBJECT_ID) == newMovingObject

    def test_update_not_existent_moving_object(self):
        with raises(UnknownMovingObjectException):
            self.__moving_object_manager.update_moving_object(object_id="missingMovingObjectId", object={})

    def test_add_object_triggers_listener(self):
        expected_value = "SUCCESS"
        container = []
        self.__moving_object_manager.call_on_add(Callback(lambda v, o: container.append(expected_value), None))
        self.__moving_object_manager.add_moving_object(object_id=self.__MOVING_OBJECT_ID,
                                                       object=self.__test_moving_object)
        assert len(container) > 0
        assert container[0] is expected_value

    def test_remove_object_triggers_listener(self):
        expected_value = "SUCCESS"
        container = []
        self.__moving_object_manager.call_on_remove(Callback(lambda v, o: container.append(expected_value), None))
        self.__moving_object_manager.add_moving_object(object_id=self.__MOVING_OBJECT_ID,
                                                       object=self.__test_moving_object)
        self.__moving_object_manager.remove_moving_object(object_id=self.__MOVING_OBJECT_ID)
        assert len(container) > 0
        assert container[0] is expected_value

    def test_register_multiple_triggers_on_add(self):
        expected_value = "SUCCESS"
        total = 100
        container = []
        for i in range(total):
            self.__moving_object_manager.call_on_add(Callback(lambda x, o: container.append(expected_value), None))
        self.__moving_object_manager.add_moving_object(object_id=self.__MOVING_OBJECT_ID,
                                                       object=self.__test_moving_object)
        assert len(container) == total
        for i in range(total):
            assert container[i] == expected_value

    def test_register_multiple_triggers_on_remove(self):
        expected_value = "SUCCESS"
        total = 100
        container = []
        for i in range(total):
            self.__moving_object_manager.call_on_remove(Callback(lambda x, o: container.append(expected_value), None))
        self.__moving_object_manager.add_moving_object(object_id=self.__MOVING_OBJECT_ID,
                                                       object=self.__test_moving_object)
        self.__moving_object_manager.remove_moving_object(object_id=self.__MOVING_OBJECT_ID)
        assert len(container) == total
        for i in range(total):
            assert container[i] == expected_value

    def test_on_add_failure_rollbacks(self):
        container = {
            1 : {"executed": False, "rolledback" : False},
            2 : {"executed": False, "rolledback" : False},
            3 : {"executed": False, "rolledback" : False},
         }
        callback1 = lambda v, o: container[1].update({"executed": True})
        rollback1 = lambda v, o: container[1].update({"rolledback" : True })
        callback2 = lambda v, o: 1 / 0  # should raise exception
        callback3 = lambda v, o: container[3].update({"executed": True})
        rollback3 = lambda v, o: container[3].update({"rolledback": True})

        self.__moving_object_manager.call_on_add(Callback(callback1, rollback1))
        self.__moving_object_manager.call_on_add(Callback(callback2, None))
        self.__moving_object_manager.call_on_add(Callback(callback3, rollback3))

        with raises(ArithmeticError):
            self.__moving_object_manager.add_moving_object(object_id=self.__MOVING_OBJECT_ID,
                                                       object=self.__test_moving_object)

        assert not self.__moving_object_manager.get_all_moving_objects()
        assert container[1]["executed"] is True
        assert container[3]["executed"] is False
        assert container[1]["rolledback"] is True
        assert container[3]["rolledback"] is False

    def test_on_remove_failure_rollbacks(self):
        container = {
            1 : {"executed": False, "rolledback" : False},
            2 : {"executed": False, "rolledback" : False},
            3 : {"executed": False, "rolledback" : False},
         }
        callback1 = lambda v, o: container[1].update({"executed": True})
        rollback1 = lambda v, o: container[1].update({"rolledback" : True })
        callback2 = lambda v, o: 1 / 0  # should raise exception
        callback3 = lambda v, o: container[3].update({"executed": True})
        rollback3 = lambda v, o: container[3].update({"rolledback": True})

        self.__moving_object_manager.call_on_remove(Callback(callback1, rollback1))
        self.__moving_object_manager.call_on_remove(Callback(callback2, None))
        self.__moving_object_manager.call_on_remove(Callback(callback3, rollback3))

        self.__moving_object_manager.add_moving_object(object_id=self.__MOVING_OBJECT_ID, object=self.__test_moving_object)

        with raises(ArithmeticError):
            self.__moving_object_manager.remove_moving_object(object_id=self.__MOVING_OBJECT_ID)

        assert self.__test_moving_object in self.__moving_object_manager.get_all_moving_objects()
        assert container[1]["executed"] is True
        assert container[3]["executed"] is False
        assert container[1]["rolledback"] is True
        assert container[3]["rolledback"] is False
