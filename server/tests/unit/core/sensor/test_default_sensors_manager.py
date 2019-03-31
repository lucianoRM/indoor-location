from pytest import fixture, raises

from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.object.kvdb_moving_objects_manager import KVDBMovingObjectsManager
from src.core.object.kvdb_static_objects_manager import KVDBStaticObjectsManager
from src.core.sensor.default_sensors_manager import DefaultSensorsManager
from src.core.sensor.sensors_manager import SensorAlreadyExistsException, UnknownSensorException
from tests.unit.test_implementations.implementations import TestStaticSensor, TestMovingSensor


class TestDefaultSensorsManager:

    __STATIC_SENSOR_ID = "static_sensor_id"
    __MOVING_SENSOR_ID = "moving_sensor_id"

    @fixture(autouse=True)
    def setUp(self):
        self.__test_static_sensor = TestStaticSensor(id=self.__STATIC_SENSOR_ID, position=None)
        self.__test_moving_sensor = TestMovingSensor(id=self.__MOVING_SENSOR_ID, position=None)
        db = MemoryKVDatabase()
        self.__sensors_manager = DefaultSensorsManager(
            static_objects_manager=KVDBStaticObjectsManager(kv_database=db),
            moving_objects_manager=KVDBMovingObjectsManager(kv_database=db)
        )

    def test_add_sensor(self):
        self.__sensors_manager.add_sensor(sensor_id=self.__MOVING_SENSOR_ID, sensor=self.__test_moving_sensor)
        self.__sensors_manager.add_sensor(sensor_id=self.__STATIC_SENSOR_ID, sensor=self.__test_static_sensor)
        assert self.__sensors_manager.get_sensor(self.__STATIC_SENSOR_ID) == self.__test_static_sensor
        assert self.__sensors_manager.get_sensor(self.__MOVING_SENSOR_ID) == self.__test_moving_sensor

    def test_add_sensor_with_same_id(self):
        self.__sensors_manager.add_sensor(sensor_id=self.__STATIC_SENSOR_ID, sensor=self.__test_static_sensor)
        sameIdSensor = TestStaticSensor(id=self.__STATIC_SENSOR_ID, position=None)
        with raises(SensorAlreadyExistsException):
            self.__sensors_manager.add_sensor(sensor_id=self.__STATIC_SENSOR_ID, sensor=sameIdSensor)

    def test_add_multiple_sensors_and_get_all(self):
        all_sensors = []
        for i in range(100):
            id = str(i)
            sensor = TestStaticSensor(id=id, position=None) if i % 2 == 0 else TestMovingSensor(id=id, position=None)
            all_sensors.append(sensor)
            self.__sensors_manager.add_sensor(sensor_id=id, sensor=sensor)
        retrieved_sensors = self.__sensors_manager.get_all_sensors()
        for sensor in all_sensors:
            assert sensor in retrieved_sensors

    def test_remove_sensor_and_try_get_it(self):
        self.__sensors_manager.add_sensor(sensor_id=self.__STATIC_SENSOR_ID, sensor=self.__test_static_sensor)
        assert self.__sensors_manager.get_sensor(self.__STATIC_SENSOR_ID) == self.__test_static_sensor
        self.__sensors_manager.remove_sensor(self.__STATIC_SENSOR_ID)
        with raises(UnknownSensorException):
            self.__sensors_manager.get_sensor(sensor_id=self.__STATIC_SENSOR_ID)

    def test_get_sensor_from_empty_db(self):
        with raises(UnknownSensorException):
            self.__sensors_manager.get_sensor(sensor_id=self.__STATIC_SENSOR_ID)

    def test_update_sensor(self):
        self.__sensors_manager.add_sensor(self.__STATIC_SENSOR_ID, self.__test_static_sensor)
        newSensor = TestStaticSensor(id=self.__STATIC_SENSOR_ID, position="newPosition")
        self.__sensors_manager.update_sensor(self.__STATIC_SENSOR_ID,
                                             newSensor)
        assert self.__sensors_manager.get_sensor(self.__STATIC_SENSOR_ID) == newSensor

    def test_update_not_existent_sensor(self):
        with raises(UnknownSensorException):
            self.__sensors_manager.update_sensor(sensor_id="missingSensorId", sensor={})
