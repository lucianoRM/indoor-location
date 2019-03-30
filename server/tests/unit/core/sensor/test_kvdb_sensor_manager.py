from pytest import fixture, raises

from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.sensor.kvdb_sensor_manager import KVDBSensor
from src.core.sensor.sensor_manager import SensorAlreadyExistsException, UnknownSensorException
from tests.unit.test_implementations.implementations import TestSensor


class TestKVDBSensorManager:

    __SENSOR_ID = "sensor_name"
    __SENSOR_NAME = "sensor_name"

    @fixture(autouse=True)
    def setUp(self):
        self.__test_sensor = TestSensor(name=self.__SENSOR_NAME)
        self.__sensor_manager = KVDBSensor(MemoryKVDatabase())

    def test_add_sensor(self):
        self.__sensor_manager.add_sensor(sensor_id=self.__SENSOR_ID, sensor=self.__test_sensor)
        assert self.__sensor_manager.get_sensor(self.__SENSOR_ID) == self.__test_sensor

    def test_add_sensor_with_same_id(self):
        self.__sensor_manager.add_sensor(sensor_id=self.__SENSOR_ID, sensor=self.__test_sensor)
        sameIdSensor = TestSensor(name=self.__SENSOR_NAME)
        with raises(SensorAlreadyExistsException):
            self.__sensor_manager.add_sensor(sensor_id=self.__SENSOR_ID, sensor=sameIdSensor)

    def test_add_multiple_sensors_and_get_all(self):
        all_sensors = []
        for i in range(100):
            id = str(i)
            sensor = TestSensor(name=id)
            all_sensors.append(sensor)
            self.__sensor_manager.add_sensor(sensor_id=id, sensor=sensor)
        retrieved_sensors = self.__sensor_manager.get_all_sensors()
        for sensor in all_sensors:
            assert sensor in retrieved_sensors

    def test_remove_sensor_and_try_get_it(self):
        self.__sensor_manager.add_sensor(sensor_id=self.__SENSOR_ID, sensor=self.__test_sensor)
        assert self.__sensor_manager.get_sensor(self.__SENSOR_ID) == self.__test_sensor
        self.__sensor_manager.remove_sensor(self.__SENSOR_ID)
        with raises(UnknownSensorException):
            self.__sensor_manager.get_sensor(sensor_id=self.__SENSOR_ID)

    def test_get_sensor_from_empty_db(self):
        with raises(UnknownSensorException):
            self.__sensor_manager.get_sensor(sensor_id=self.__SENSOR_ID)

    def test_update_sensor(self):
        self.__sensor_manager.add_sensor(self.__SENSOR_ID, self.__test_sensor)
        newSensor = TestSensor(name="newName")
        self.__sensor_manager.update_sensor(self.__SENSOR_ID,
                                            newSensor)
        assert self.__sensor_manager.get_sensor(self.__SENSOR_ID) == newSensor

    def test_update_not_existent_sensor(self):
        with raises(UnknownSensorException):
            self.__sensor_manager.update_sensor(sensor_id="missingSensorId", sensor={})
