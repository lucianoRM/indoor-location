from pytest import fixture, raises

from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.emitter.default_signal_emitters_manager import DefaultSignalEmittersManager
from src.core.emitter.signal_emitters_manager import SignalEmitterAlreadyExistsException, UnknownSignalEmitterException
from src.core.manager.default_positionable_objects_manager import PositionableObjectsManagerObserver
from src.core.object.kvdb_moving_objects_manager import KVDBMovingObjectsManager
from src.core.object.kvdb_static_objects_manager import KVDBStaticObjectsManager
from tests.unit.test_implementations.implementations import FakeAnchor, FakeUser, FakeSignalEmitter


class TestDefaultSignalEmittersManager:
    __STATIC_SIGNAL_EMITTER_ID = "static_signal_emitter_id"
    __MOVING_SIGNAL_EMITTER_ID = "moving_signal_emitter_id"

    @fixture(autouse=True)
    def setUp(self):
        db = MemoryKVDatabase()

        self.__fake_static_object_id = "static_object"
        self.__fake_static_object = FakeAnchor(self.__fake_static_object_id, "position")

        self.__fake_moving_object_id = "moving_object"
        self.__fake_moving_object = FakeUser(self.__fake_moving_object_id, "position")

        self.__static_objects_manager = KVDBStaticObjectsManager(kv_database=db)
        self.__moving_objects_manager = KVDBMovingObjectsManager(kv_database=db)
        observer = PositionableObjectsManagerObserver(
            observable_static_objects_manager=self.__static_objects_manager,
            observable_moving_objects_manager=self.__moving_objects_manager
        )
        self.__signal_emitters_manager = DefaultSignalEmittersManager(objects_manager=observer)

    def test_add_static_object_and_get_signal_emitters(self):
        s1_id = "s1"
        s1 = FakeSignalEmitter(s1_id)
        s2_id = "s2"
        s2 = FakeSignalEmitter(s2_id)

        self.__fake_static_object.add_signal_emitter(s1_id, s1)
        self.__fake_static_object.add_signal_emitter(s2_id, s2)
        self.__static_objects_manager.add_static_object(object_id=self.__fake_static_object_id,
                                                        object=self.__fake_static_object)

        assert self.__signal_emitters_manager.get_signal_emitter(s1_id) == s1
        assert self.__signal_emitters_manager.get_signal_emitter(s2_id) == s2
        all_signal_emitters = self.__signal_emitters_manager.get_all_signal_emitters()
        assert s1 in all_signal_emitters
        assert s2 in all_signal_emitters

    def test_add_moving_object_and_get_signal_emitters(self):
        s1_id = "s1"
        s1 = FakeSignalEmitter(s1_id)
        s2_id = "s2"
        s2 = FakeSignalEmitter(s2_id)

        self.__fake_moving_object.add_signal_emitter(s1_id, s1)
        self.__fake_moving_object.add_signal_emitter(s2_id, s2)
        self.__moving_objects_manager.add_moving_object(object_id=self.__fake_moving_object_id,
                                                        object=self.__fake_moving_object)

        assert self.__signal_emitters_manager.get_signal_emitter(s1_id) == s1
        assert self.__signal_emitters_manager.get_signal_emitter(s2_id) == s2
        all_signal_emitters = self.__signal_emitters_manager.get_all_signal_emitters()
        assert s1 in all_signal_emitters
        assert s2 in all_signal_emitters

    def test_add_signal_emitter_with_same_id(self):
        s1_id = "s1"
        s1 = FakeSignalEmitter(id=s1_id)

        self.__fake_moving_object.add_signal_emitter(s1_id, s1)
        self.__fake_static_object.add_signal_emitter(s1_id, s1)

        self.__moving_objects_manager.add_moving_object(object_id=self.__fake_moving_object_id,
                                                        object=self.__fake_moving_object)

        with raises(SignalEmitterAlreadyExistsException):
            self.__static_objects_manager.add_static_object(object_id=self.__fake_static_object_id,
                                                            object=self.__fake_static_object)

        assert not self.__static_objects_manager.get_all_static_objects()

    def test_add_multiple_objects_and_get_all_signal_emitters(self):
        all_signal_emitters = []
        for i in range(0, 100):
            moving_object_id = str(i)
            moving_signal_emitter_id = str(100 + i)
            static_object_id = str(200 + i)
            static_signal_emitter_id = str(300 + i)

            user = FakeUser(id=moving_object_id, position=None)
            user_signal_emitter = FakeSignalEmitter(id=moving_signal_emitter_id)
            user.add_signal_emitter(moving_signal_emitter_id, user_signal_emitter)

            self.__moving_objects_manager.add_moving_object(moving_signal_emitter_id, user)

            anchor = FakeAnchor(id=static_object_id, position=None)
            anchor_signal_emitter = FakeSignalEmitter(id=static_signal_emitter_id)
            anchor.add_signal_emitter(static_signal_emitter_id, anchor_signal_emitter)

            self.__static_objects_manager.add_static_object(static_object_id, anchor)

            all_signal_emitters.append(anchor_signal_emitter)
            all_signal_emitters.append(user_signal_emitter)

        retrieved_signal_emitters = self.__signal_emitters_manager.get_all_signal_emitters()
        for signal_emitter in all_signal_emitters:
            assert signal_emitter in retrieved_signal_emitters

    def test_get_signal_emitter_from_empty_db(self):
        with raises(UnknownSignalEmitterException):
            self.__signal_emitters_manager.get_signal_emitter(signal_emitter_id=self.__STATIC_SIGNAL_EMITTER_ID)

    def test_update_object_changes_signal_emitter_on_static_object(self):
        s1_id = "s1"
        s1 = FakeSignalEmitter(s1_id, signal="version1")

        so_id = "static_object"
        static_object = FakeAnchor(id=so_id, position=None)
        static_object.add_signal_emitter(s1_id, s1)
        self.__static_objects_manager.add_static_object(so_id, static_object)

        assert self.__signal_emitters_manager.get_signal_emitter(s1_id) == s1

        s2 = FakeSignalEmitter(s1_id, signal="version2")
        static_object = FakeAnchor(id=so_id, position=None)
        static_object.add_signal_emitter(s1_id, s2)
        self.__static_objects_manager.update_static_object(so_id, static_object)

        assert self.__signal_emitters_manager.get_signal_emitter(s1_id) == s2

    def test_update_object_with_new_se(self):
        so_id = "static_object"
        static_object = FakeAnchor(id=so_id, position=None)
        self.__static_objects_manager.add_static_object(so_id, static_object)

        assert not self.__signal_emitters_manager.get_all_signal_emitters()

        se_id = "se_id"
        se = FakeSignalEmitter(se_id)
        static_object = FakeAnchor(id=so_id, position=None)
        static_object.add_signal_emitter(se_id, se)
        self.__static_objects_manager.update_static_object(so_id, static_object)

        assert self.__signal_emitters_manager.get_signal_emitter(se_id) == se
