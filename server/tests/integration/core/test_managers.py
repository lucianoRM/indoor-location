from pytest import fixture, raises

from src.core.anchor.anchors_manager import UnknownAnchorException, AnchorAlreadyExistsException
from src.core.anchor.default_anchors_manager import DefaultAnchorsManager
from src.core.anchor.sensing_anchor import SensingAnchor
from src.core.anchor.signal_emitting_anchor import SignalEmittingAnchor
from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.emitter.default_signal_emitters_manager import DefaultSignalEmittersManager
from src.core.emitter.signal_emitters_manager import UnknownSignalEmitterException, SignalEmitterAlreadyExistsException
from src.core.manager.default_positionable_objects_manager import PositionableObjectsManagerObserver
from src.core.object.kvdb_moving_objects_manager import KVDBMovingObjectsManager
from src.core.object.kvdb_static_objects_manager import KVDBStaticObjectsManager
from src.core.sensor.default_sensors_manager import DefaultSensorsManager
from src.core.sensor.sensors_manager import UnknownSensorException, SensorAlreadyExistsException
from src.core.user.default_users_manager import DefaultUsersManager
from src.core.user.sensing_user import SensingUser
from src.core.user.signal_emitting_user import SignalEmittingUser
from src.core.user.users_manager import UnknownUserException, UserAlreadyExistsException


class TestManagers:

    @fixture(autouse=True)
    def set_up(self):
        database = MemoryKVDatabase()
        static_objects_manager = KVDBStaticObjectsManager(kv_database=database)
        moving_objects_manager = KVDBMovingObjectsManager(kv_database=database)

        objects_manager_for_sensors = PositionableObjectsManagerObserver(observable_static_objects_manager=static_objects_manager, observable_moving_objects_manager=moving_objects_manager)
        objects_manager_for_signal_emitters = PositionableObjectsManagerObserver(observable_static_objects_manager=static_objects_manager, observable_moving_objects_manager=moving_objects_manager)

        self.__users_manager = DefaultUsersManager(moving_objects_manager=moving_objects_manager)
        self.__sensors_manager = DefaultSensorsManager(objects_manager=objects_manager_for_sensors)
        self.__anchors_manager = DefaultAnchorsManager(static_objects_manager=static_objects_manager)
        self.__signal_emitters_manager = DefaultSignalEmittersManager(objects_manager=objects_manager_for_signal_emitters)

    def test_add_user_and_get_sensor(self):
        user_id = "id"
        sensing_user = SensingUser(id=user_id, position="position")
        self.__users_manager.add_user(user_id=user_id, user=sensing_user)
        sensor = self.__sensors_manager.remove_sensor(sensor_id=user_id)
        assert sensor == sensing_user
        with raises(UnknownUserException):
            self.__users_manager.get_user(user_id=user_id)

    def test_add_sensor_and_get_user(self):
        sensor_id = "id"
        sensing_user = SensingUser(id=sensor_id, position="position")
        self.__sensors_manager.add_sensor(sensor_id=sensor_id, sensor=sensing_user)
        user = self.__users_manager.remove_user(user_id=sensor_id)
        assert user == sensing_user
        with raises(UnknownSensorException):
            self.__sensors_manager.get_sensor(sensor_id=sensor_id)

    def test_add_user_and_sensor_with_same_id(self):
        user_id = "id"
        user = SensingUser(id=user_id, position="position")
        self.__users_manager.add_user(user_id=user_id, user=user)
        with raises(SensorAlreadyExistsException):
            self.__sensors_manager.add_sensor(sensor_id=user_id, sensor=user)

    def test_add_sensor_and_user_with_same_id(self):
        sensor_id = "id"
        sensor = SensingUser(id=sensor_id, position="position")
        self.__sensors_manager.add_sensor(sensor_id=sensor_id, sensor=sensor)
        with raises(UserAlreadyExistsException):
            self.__users_manager.add_user(user_id=sensor_id, user=sensor)

    def test_add_user_and_sensor_and_get_both(self):
        user = SensingUser(id="user_id", position="position")
        sensor = SensingUser(id="sensor_id", position="position")
        self.__users_manager.add_user(user_id=user.id, user=user)
        self.__sensors_manager.add_sensor(sensor_id=sensor.id, sensor=sensor)
        users = self.__users_manager.get_all_users()
        sensors = self.__sensors_manager.get_all_sensors()
        assert len(users) == 2
        assert len(sensors) == 2

    def test_signal_emitting_user_not_a_sensor(self):
        user = SignalEmittingUser(id="se_id", position="position")
        self.__users_manager.add_user(user_id=user.id, user=user)
        with raises(UnknownSensorException):
            self.__sensors_manager.get_sensor(sensor_id=user.id)

    def test_add_anchor_and_get_sensor(self):
        anchor_id = "id"
        sensing_anchor = SensingAnchor(id=anchor_id, position="position")
        self.__anchors_manager.add_anchor(anchor_id=anchor_id, anchor=sensing_anchor)
        sensor = self.__sensors_manager.remove_sensor(sensor_id=anchor_id)
        assert sensor == sensing_anchor
        with raises(UnknownAnchorException):
            self.__anchors_manager.get_anchor(anchor_id=anchor_id)

    def test_add_sensor_and_get_anchor(self):
        sensor_id = "id"
        sensing_anchor = SensingAnchor(id=sensor_id, position="position")
        self.__sensors_manager.add_sensor(sensor_id=sensor_id, sensor=sensing_anchor)
        anchor = self.__anchors_manager.remove_anchor(anchor_id=sensor_id)
        assert anchor == sensing_anchor
        with raises(UnknownSensorException):
            self.__sensors_manager.get_sensor(sensor_id=sensor_id)

    def test_add_anchor_and_sensor_with_same_id(self):
        anchor_id = "id"
        anchor = SensingAnchor(id=anchor_id, position="position")
        self.__anchors_manager.add_anchor(anchor_id=anchor_id, anchor=anchor)
        with raises(SensorAlreadyExistsException):
            self.__sensors_manager.add_sensor(sensor_id=anchor_id, sensor=anchor)

    def test_add_sensor_and_anchor_with_same_id(self):
        sensor_id = "id"
        sensor = SensingAnchor(id=sensor_id, position="position")
        self.__sensors_manager.add_sensor(sensor_id=sensor_id, sensor=sensor)
        with raises(AnchorAlreadyExistsException):
            self.__anchors_manager.add_anchor(anchor_id=sensor_id, anchor=sensor)

    def test_add_anchor_and_sensor_and_get_both(self):
        anchor = SensingAnchor(id="anchor_id", position="position")
        sensor = SensingAnchor(id="sensor_id", position="position")
        self.__anchors_manager.add_anchor(anchor_id=anchor.id, anchor=anchor)
        self.__sensors_manager.add_sensor(sensor_id=sensor.id, sensor=sensor)
        anchors = self.__anchors_manager.get_all_anchors()
        sensors = self.__sensors_manager.get_all_sensors()
        assert len(anchors) == 2
        assert len(sensors) == 2

    def test_signal_emitting_anchor_not_a_sensor(self):
        anchor = SignalEmittingAnchor(id="se_id", position="position")
        self.__anchors_manager.add_anchor(anchor_id=anchor.id, anchor=anchor)
        with raises(UnknownSensorException):
            self.__sensors_manager.get_sensor(sensor_id=anchor.id)

    def test_add_user_and_get_signal_emitter(self):
        user_id = "id"
        se_user = SignalEmittingUser(id=user_id, position="position")
        self.__users_manager.add_user(user_id=user_id, user=se_user)
        signal_emitter = self.__signal_emitters_manager.remove_signal_emitter(signal_emitter_id=user_id)
        assert signal_emitter == se_user
        with raises(UnknownUserException):
            self.__users_manager.get_user(user_id=user_id)

    def test_add_signal_emitter_and_get_user(self):
        signal_emitter_id = "id"
        se_user = SignalEmittingUser(id=signal_emitter_id, position="position")
        self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=signal_emitter_id, signal_emitter=se_user)
        user = self.__users_manager.remove_user(user_id=signal_emitter_id)
        assert user == se_user
        with raises(UnknownSignalEmitterException):
            self.__signal_emitters_manager.get_signal_emitter(signal_emitter_id=signal_emitter_id)

    def test_add_user_and_signal_emitter_with_same_id(self):
        user_id = "id"
        user = SignalEmittingUser(id=user_id, position="position")
        self.__users_manager.add_user(user_id=user_id, user=user)
        with raises(SignalEmitterAlreadyExistsException):
            self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=user_id, signal_emitter=user)

    def test_add_signal_emitter_and_user_with_same_id(self):
        signal_emitter_id = "id"
        se = SignalEmittingUser(id=signal_emitter_id, position="position")
        self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=signal_emitter_id, signal_emitter=se)
        with raises(UserAlreadyExistsException):
            self.__users_manager.add_user(user_id=signal_emitter_id, user=se)

    def test_add_user_and_signal_emitter_and_get_both(self):
        user = SignalEmittingUser(id="user_id", position="position")
        se = SignalEmittingUser(id="se_id", position="position")
        self.__users_manager.add_user(user_id=user.id, user=user)
        self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=se.id, signal_emitter=se)
        users = self.__users_manager.get_all_users()
        sensors = self.__signal_emitters_manager.get_all_signal_emitters()
        assert len(users) == 2
        assert len(sensors) == 2

    def test_sensing_user_not_a_signal_emitter(self):
        user = SensingUser(id="sensor_id", position="position")
        self.__users_manager.add_user(user_id=user.id, user=user)
        with raises(UnknownSignalEmitterException):
            self.__signal_emitters_manager.get_signal_emitter(signal_emitter_id=user.id)

    def test_add_anchor_and_get_signal_emitter(self):
        anchor_id = "id"
        se_anchor = SignalEmittingAnchor(id=anchor_id, position="position")
        self.__anchors_manager.add_anchor(anchor_id=anchor_id, anchor=se_anchor)
        signal_emitter = self.__signal_emitters_manager.remove_signal_emitter(signal_emitter_id=anchor_id)
        assert signal_emitter == se_anchor
        with raises(UnknownAnchorException):
            self.__anchors_manager.get_anchor(anchor_id=anchor_id)

    def test_add_signal_emitter_and_get_anchor(self):
        signal_emitter_id = "id"
        se_anchor = SignalEmittingAnchor(id=signal_emitter_id, position="position")
        self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=signal_emitter_id, signal_emitter=se_anchor)
        anchor = self.__anchors_manager.remove_anchor(anchor_id=signal_emitter_id)
        assert anchor == se_anchor
        with raises(UnknownSignalEmitterException):
            self.__signal_emitters_manager.get_signal_emitter(signal_emitter_id=signal_emitter_id)

    def test_add_anchor_and_signal_emitter_with_same_id(self):
        anchor_id = "id"
        anchor = SignalEmittingAnchor(id=anchor_id, position="position")
        self.__anchors_manager.add_anchor(anchor_id=anchor_id, anchor=anchor)
        with raises(SignalEmitterAlreadyExistsException):
            self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=anchor_id, signal_emitter=anchor)

    def test_add_signal_emitter_and_anchor_with_same_id(self):
        signal_emitter_id = "id"
        se = SignalEmittingAnchor(id=signal_emitter_id, position="position")
        self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=signal_emitter_id, signal_emitter=se)
        with raises(AnchorAlreadyExistsException):
            self.__anchors_manager.add_anchor(anchor_id=signal_emitter_id, anchor=se)

    def test_add_anchor_and_signal_emitter_and_get_both(self):
        anchor = SignalEmittingAnchor(id="anchor_id", position="position")
        se = SignalEmittingAnchor(id="se_id", position="position")
        self.__anchors_manager.add_anchor(anchor_id=anchor.id, anchor=anchor)
        self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=se.id, signal_emitter=se)
        anchors = self.__anchors_manager.get_all_anchors()
        sensors = self.__signal_emitters_manager.get_all_signal_emitters()
        assert len(anchors) == 2
        assert len(sensors) == 2

    def test_sensing_anchor_not_a_signal_emitter(self):
        anchor = SensingAnchor(id="sensor_id", position="position")
        self.__anchors_manager.add_anchor(anchor_id=anchor.id, anchor=anchor)
        with raises(UnknownSignalEmitterException):
            self.__signal_emitters_manager.get_signal_emitter(signal_emitter_id=anchor.id)

    def test_add_anchor_and_user_and_get_sensors(self):
        anchor = SensingAnchor(id="a_id", position="position")
        user = SensingUser(id="u_id",position="position")
        self.__anchors_manager.add_anchor(anchor_id=anchor.id, anchor=anchor)
        self.__users_manager.add_user(user_id=user.id, user=user)
        assert len(self.__sensors_manager.get_all_sensors()) == 2
        assert len(self.__anchors_manager.get_all_anchors()) == 1
        assert len(self.__users_manager.get_all_users()) == 1

    def test_add_anchor_and_user_and_get_signal_emitters(self):
        anchor = SignalEmittingAnchor(id="a_id", position="position")
        user = SignalEmittingUser(id="u_id",position="position")
        self.__anchors_manager.add_anchor(anchor_id=anchor.id, anchor=anchor)
        self.__users_manager.add_user(user_id=user.id, user=user)
        assert len(self.__signal_emitters_manager.get_all_signal_emitters()) == 2
        assert len(self.__anchors_manager.get_all_anchors()) == 1
        assert len(self.__users_manager.get_all_users()) == 1

    def test_add_sensor_and_update_signal_emitter(self):
        sensor = SensingUser(id="id", position="position")
        self.__sensors_manager.add_sensor(sensor_id=sensor.id, sensor=sensor)
        with raises(UnknownSignalEmitterException):
            self.__signal_emitters_manager.update_signal_emitter(signal_emitter_id=sensor.id, signal_emitter=SignalEmittingUser(id="otherId", position="none"))
