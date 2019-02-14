from unittest import TestCase

from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.sensor.sensor import Sensor, ID_KEY, NAME_KEY, LOCATION_KEY
from src.core.sensor.kvdb_sensor_manager import KVDBSensorManager
from src.core.sensor.sensor_manager import SensorAlreadyExistsException, UnknownSensorException


class KVDBSensorManagerTestCase(TestCase):

    __SENSOR_ID = "sensorId"

    def setUp(self):
        self.__test_sensor = Sensor(**{ID_KEY : self.__SENSOR_ID,
                                     NAME_KEY : "sensorName",
                                     LOCATION_KEY : (0,0)})
        self.__sensor_manager = KVDBSensorManager(MemoryKVDatabase())

    def test_add_sensor(self):
        self.__sensor_manager.add_sensor(self.__test_sensor)
        self.assertEquals(self.__sensor_manager.get_sensor(self.__SENSOR_ID), self.__test_sensor)

    def test_add_sensor_with_same_id(self):
        self.__sensor_manager.add_sensor(self.__test_sensor)
        sameIdSensor = Sensor(**{ID_KEY : self.__SENSOR_ID,
                                     NAME_KEY : "otherSensor",
                                     LOCATION_KEY : (1,1)})
        self.assertRaises(SensorAlreadyExistsException,self.__sensor_manager.add_sensor, sameIdSensor)

    def test_add_multiple_sensors_and_get_all(self):
        all_sensors = [Sensor(**{ID_KEY:str(sensorId), NAME_KEY:"sensorName", LOCATION_KEY: (0,0)}) for sensorId in xrange(100)]
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
        newSensor = Sensor(**{ID_KEY : self.__SENSOR_ID,
                              NAME_KEY : "newSensorName",
                              LOCATION_KEY : (1,1)})
        self.__sensor_manager.update_sensor(self.__SENSOR_ID,
                                            newSensor)
        self.assertEquals(self.__sensor_manager.get_sensor(self.__SENSOR_ID), newSensor)

    def test_update_not_existent_sensor(self):
        self.assertRaises(UnknownSensorException,self.__sensor_manager.update_sensor, "missingSensorId", {})
