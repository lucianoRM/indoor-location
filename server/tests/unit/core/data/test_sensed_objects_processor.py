from unittest import TestCase

from measurement.measures import Distance
from mock import Mock

from src.core.data.kvdb_sensed_objects_processor import KVDBSensedObjectsProcessor
from src.core.data.sensing_data import SensingData
from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.sensor.sensor import Sensor


class SensedObjectsProcessorUnitTest(TestCase):

    def setUp(self):
        __database = MemoryKVDatabase()

        self.__user_manager = Mock()
        self.__sensor_manager = Mock()
        self.__location_service = Mock()

        self.__processor = KVDBSensedObjectsProcessor(database=__database, user_manager=self.__user_manager , sensor_manager=self.__sensor_manager, location_service=self.__location_service)

    def test_sensor_information_is_added(self):
        sensed_object_id = 1
        sensed_object_information = SensingData(distance=Distance(m=10), timestamp=1)

        sensor_id = 1
        sensor = Sensor(id=sensor_id, position=10)
        self.__sensor_manager.get_sensor.side_effect = (lambda id : sensor)

        self.__processor.process_new_data(sensor_id,{sensed_object_id: sensed_object_information})

        self.assertTrue(len(sensor.get_sensed_objects()) == 1)
        self.assertEquals(sensor.get_sensed_objects().get(sensed_object_id).distance, sensed_object_information.distance)

    def test_sensor_information_is_removed(self):
        sensed_object_id = 1
        sensed_object_information = SensingData(distance=Distance(m=10), timestamp=1)

        sensor_id = 1
        sensor = Sensor(id=sensor_id, position=10)
        self.__sensor_manager.get_sensor.side_effect = (lambda id: sensor)

        self.__processor.process_new_data(sensor_id, {sensed_object_id: sensed_object_information})

        self.assertTrue(len(sensor.get_sensed_objects()) == 1)
        self.assertEquals(sensor.get_sensed_objects().get(sensed_object_id).distance,sensed_object_information.distance)

        sensed_object_id2 = 2
        sensed_object_information2 = SensingData(distance=Distance(m=20), timestamp=1)
        self.__processor.process_new_data(sensor_id, {sensed_object_id2: sensed_object_information2})

        self.assertTrue(len(sensor.get_sensed_objects()) == 1)
        self.assertEquals(sensor.get_sensed_objects().get(sensed_object_id2).distance,sensed_object_information2.distance)

    def test_sensor_information_is_updated(self):
        sensed_object_id = 1
        sensed_object_information = SensingData(distance=Distance(m=10), timestamp=1)

        sensor_id = 1
        sensor = Sensor(id=sensor_id, position=10)
        self.__sensor_manager.get_sensor.side_effect = (lambda id: sensor)

        self.__processor.process_new_data(sensor_id, {sensed_object_id: sensed_object_information})

        self.assertTrue(len(sensor.get_sensed_objects()) == 1)
        self.assertEquals(sensor.get_sensed_objects().get(sensed_object_id).distance,
                          sensed_object_information.distance)

        sensed_object_information2 = SensingData(distance=Distance(m=20), timestamp=1)
        self.__processor.process_new_data(sensor_id, {sensed_object_id : sensed_object_information2})

        self.assertTrue(len(sensor.get_sensed_objects()) == 1)
        self.assertEquals(sensor.get_sensed_objects().get(sensed_object_id).distance,sensed_object_information2.distance)




