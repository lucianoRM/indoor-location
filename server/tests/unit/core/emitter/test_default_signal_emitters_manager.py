

from pytest import fixture, raises

from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.emitter.default_signal_emitters_manager import DefaultSignalEmittersManager
from src.core.emitter.signal_emitters_manager import SignalEmitterAlreadyExistsException, UnknownSignalEmitterException
from src.core.manager.observer_composed_objects_manager import ObserverComposedObjectsManager
from src.core.object.kvdb_moving_objects_manager import KVDBMovingObjectsManager
from src.core.object.kvdb_static_objects_manager import KVDBStaticObjectsManager
from tests.unit.test_implementations.implementations import TestStaticSignalEmitter, TestMovingSignalEmitter


class TestDefaultSignalEmittersManager:

    __STATIC_SIGNAL_EMITTER_ID = "static_signal_emitter_id"
    __MOVING_SIGNAL_EMITTER_ID = "moving_signal_emitter_id"

    @fixture(autouse=True)
    def setUp(self):
        self.__test_static_signal_emitter = TestStaticSignalEmitter(id=self.__STATIC_SIGNAL_EMITTER_ID, position=None)
        self.__test_moving_signal_emitter = TestMovingSignalEmitter(id=self.__MOVING_SIGNAL_EMITTER_ID, position=None)
        db = MemoryKVDatabase()
        self.__signal_emitters_manager = DefaultSignalEmittersManager(
            ObserverComposedObjectsManager(
                observable_static_objects_manager=KVDBStaticObjectsManager(kv_database=db),
                observable_moving_objects_manager=KVDBMovingObjectsManager(kv_database=db)
            )
        )

    def test_add_signal_emitter(self):
        self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=self.__MOVING_SIGNAL_EMITTER_ID, signal_emitter=self.__test_moving_signal_emitter)
        self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=self.__STATIC_SIGNAL_EMITTER_ID, signal_emitter=self.__test_static_signal_emitter)
        assert self.__signal_emitters_manager.get_signal_emitter(self.__STATIC_SIGNAL_EMITTER_ID) == self.__test_static_signal_emitter
        assert self.__signal_emitters_manager.get_signal_emitter(self.__MOVING_SIGNAL_EMITTER_ID) == self.__test_moving_signal_emitter

    def test_add_signal_emitter_with_same_id(self):
        self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=self.__STATIC_SIGNAL_EMITTER_ID, signal_emitter=self.__test_static_signal_emitter)
        sameIdSensor = TestStaticSignalEmitter(id=self.__STATIC_SIGNAL_EMITTER_ID, position=None)
        with raises(SignalEmitterAlreadyExistsException):
            self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=self.__STATIC_SIGNAL_EMITTER_ID, signal_emitter=sameIdSensor)

    def test_add_multiple_signal_emitters_and_get_all(self):
        all_signal_emitters = []
        for i in range(100):
            id = str(i)
            signal_emitter = TestStaticSignalEmitter(id=id, position=None) if i % 2 == 0 else TestMovingSignalEmitter(id=id, position=None)
            all_signal_emitters.append(signal_emitter)
            self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=id, signal_emitter=signal_emitter)
        retrieved_signal_emitters = self.__signal_emitters_manager.get_all_signal_emitters()
        for signal_emitter in all_signal_emitters:
            assert signal_emitter in retrieved_signal_emitters

    def test_remove_signal_emitter_and_try_get_it(self):
        self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=self.__STATIC_SIGNAL_EMITTER_ID, signal_emitter=self.__test_static_signal_emitter)
        assert self.__signal_emitters_manager.get_signal_emitter(self.__STATIC_SIGNAL_EMITTER_ID) == self.__test_static_signal_emitter
        self.__signal_emitters_manager.remove_signal_emitter(self.__STATIC_SIGNAL_EMITTER_ID)
        with raises(UnknownSignalEmitterException):
            self.__signal_emitters_manager.get_signal_emitter(signal_emitter_id=self.__STATIC_SIGNAL_EMITTER_ID)

    def test_get_signal_emitter_from_empty_db(self):
        with raises(UnknownSignalEmitterException):
            self.__signal_emitters_manager.get_signal_emitter(signal_emitter_id=self.__STATIC_SIGNAL_EMITTER_ID)

    def test_update_signal_emitter(self):
        self.__signal_emitters_manager.add_signal_emitter(self.__STATIC_SIGNAL_EMITTER_ID, self.__test_static_signal_emitter)
        newSensor = TestStaticSignalEmitter(id=self.__STATIC_SIGNAL_EMITTER_ID, position="newPosition")
        self.__signal_emitters_manager.update_signal_emitter(self.__STATIC_SIGNAL_EMITTER_ID,
                                                             newSensor)
        assert self.__signal_emitters_manager.get_signal_emitter(self.__STATIC_SIGNAL_EMITTER_ID) == newSensor

    def test_update_not_existent_signal_emitter(self):
        with raises(UnknownSignalEmitterException):
            self.__signal_emitters_manager.update_signal_emitter(signal_emitter_id="missingSensorId", signal_emitter={})
