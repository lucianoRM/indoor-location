from unittest import TestCase

from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.sensor.kvdb_sensor_manager import KVDBSensor
from src.core.sensor.sensor_manager import SensorAlreadyExistsException, UnknownSensorException
from tests.unit.test_implementations.implementations import TestSensor


class KVDBSensorManagerTestCase(TestCase):

    __SENSOR_ID = "sensorId"

    def setUp(self):
        self.__test_sensor = TestSensor(id=self.__SENSOR_ID,
                                     position=(0,0),
                                     name="sensorName")
        self.__sensor_manager = KVDBSensor(MemoryKVDatabase())

    def test_add_sensor(self):
        self.__sensor_manager.add_sensor(self.__test_sensor)
        self.assertEquals(self.__sensor_manager.get_sensor(self.__SENSOR_ID), self.__test_sensor)

    def test_add_sensor_with_same_id(self):
        self.__sensor_manager.add_sensor(self.__test_sensor)
        sameIdSensor = TestSensor(id=self.__SENSOR_ID,
                              position=(1,1),
                              name="otherSensor")
        self.assertRaises(SensorAlreadyExistsException,self.__sensor_manager.add_sensor, sameIdSensor)

    def test_add_multiple_sensors_and_get_all(self):
        all_sensors = [TestSensor(id=str(sensorId), name="sensorName", position= (0,0)) for sensorId in range(100)]
        for sensor in all_sensors:
            self.__sensor_manager.add_sensor(sensor)
        retrieved_sensors = self.__sensor_manager.get_all_sensors()
        for sensor in all_sensors:
            self.assertTrue(sensor in retrieved_sensors)

    def test_remove_sensor_and_try_get_it(self):
        self.__sensor_manager.add_sensor(self.__test_sensor)
        self.assertEquals(self.__sensor_manager.get_sensor(self.__SENSOR_ID), self.__test_sensor)
        self.__sensor_manager.remove_sensor(self.__SENSOR_ID)
        self.assertRaises(UnknownSensorException, self.__sensor_manager.get_sensor, self.__SENSOR_ID)

    def test_get_sensor_from_empty_db(self):
        self.assertRaises(UnknownSensorException,self.__sensor_manager.get_sensor, self.__SENSOR_ID)

    def test_update_sensor(self):
        self.__sensor_manager.add_sensor(self.__test_sensor)
        newSensor = TestSensor(id=self.__SENSOR_ID,
                           name= "newSensorName",
                           position= (1,1))
        self.__sensor_manager.update_sensor(self.__SENSOR_ID,
                                            newSensor)
        self.assertEquals(self.__sensor_manager.get_sensor(self.__SENSOR_ID), newSensor)

    def test_update_not_existent_sensor(self):
        self.assertRaises(UnknownSensorException,self.__sensor_manager.update_sensor, "missingSensorId", {})
