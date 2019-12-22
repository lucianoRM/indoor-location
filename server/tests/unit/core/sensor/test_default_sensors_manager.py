from pytest import fixture, raises

from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.manager.default_positionable_objects_manager import PositionableObjectsManagerObserver
from src.core.object.kvdb_moving_objects_manager import KVDBMovingObjectsManager
from src.core.object.kvdb_static_objects_manager import KVDBStaticObjectsManager
from src.core.sensor.default_sensors_manager import DefaultSensorsManager
from src.core.sensor.sensors_manager import SensorAlreadyExistsException, UnknownSensorException
from tests.unit.test_implementations.implementations import FakeAnchor, FakeUser, FakeSensor


class TestDefaultSensorsManager:
    __STATIC_SENSOR_ID = "static_sensor_id"
    __MOVING_SENSOR_ID = "moving_sensor_id"

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
        self.__sensors_manager = DefaultSensorsManager(objects_manager=observer)

    def test_add_static_object_and_get_sensors(self):
        s1_id = "s1"
        s1 = FakeSensor(s1_id)
        s2_id = "s2"
        s2 = FakeSensor(s2_id)

        self.__fake_static_object.add_sensor(s1_id, s1)
        self.__fake_static_object.add_sensor(s2_id, s2)
        self.__static_objects_manager.add_static_object(object_id=self.__fake_static_object_id,
                                                        object=self.__fake_static_object)

        assert self.__sensors_manager.get_sensor(s1_id) == s1
        assert self.__sensors_manager.get_sensor(s2_id) == s2
        all_sensors = self.__sensors_manager.get_all_sensors()
        assert s1 in all_sensors
        assert s2 in all_sensors

    def test_add_moving_object_and_get_sensors(self):
        s1_id = "s1"
        s1 = FakeSensor(s1_id)
        s2_id = "s2"
        s2 = FakeSensor(s2_id)

        self.__fake_moving_object.add_sensor(s1_id, s1)
        self.__fake_moving_object.add_sensor(s2_id, s2)
        self.__moving_objects_manager.add_moving_object(object_id=self.__fake_moving_object_id,
                                                        object=self.__fake_moving_object)

        assert self.__sensors_manager.get_sensor(s1_id) == s1
        assert self.__sensors_manager.get_sensor(s2_id) == s2
        all_sensors = self.__sensors_manager.get_all_sensors()
        assert s1 in all_sensors
        assert s2 in all_sensors

    def test_add_sensor_with_same_id(self):
        s1_id = "s1"
        s1 = FakeSensor(id=s1_id)

        self.__fake_moving_object.add_sensor(s1_id, s1)
        self.__fake_static_object.add_sensor(s1_id, s1)

        self.__moving_objects_manager.add_moving_object(object_id=self.__fake_moving_object_id,
                                                        object=self.__fake_moving_object)

        with raises(SensorAlreadyExistsException):
            self.__static_objects_manager.add_static_object(object_id=self.__fake_static_object_id,
                                                            object=self.__fake_static_object)

        assert not self.__static_objects_manager.get_all_static_objects()

    def test_add_multiple_objects_and_get_all_sensors(self):
        all_sensors = []
        for i in range(0, 100):
            moving_object_id = str(i)
            moving_sensor_id = str(100 + i)
            static_object_id = str(200 + i)
            static_sensor_id = str(300 + i)

            user = FakeUser(id=moving_object_id, position=None)
            user_sensor = FakeSensor(id=moving_sensor_id)
            user.add_sensor(moving_sensor_id, user_sensor)

            self.__moving_objects_manager.add_moving_object(moving_sensor_id, user)

            anchor = FakeAnchor(id=static_object_id, position=None)
            anchor_sensor = FakeSensor(id=static_sensor_id)
            anchor.add_sensor(static_sensor_id, anchor_sensor)

            self.__static_objects_manager.add_static_object(static_object_id, anchor)

            all_sensors.append(anchor_sensor)
            all_sensors.append(user_sensor)

        retrieved_sensors = self.__sensors_manager.get_all_sensors()
        for sensor in all_sensors:
            assert sensor in retrieved_sensors

    def test_get_sensor_from_empty_db(self):
        with raises(UnknownSensorException):
            self.__sensors_manager.get_sensor(sensor_id=self.__STATIC_SENSOR_ID)
