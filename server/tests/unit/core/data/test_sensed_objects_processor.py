from unittest.mock import Mock

from measurement.measures import Distance
from pytest import fixture

from src.core.data.kvdb_sensed_objects_processor import KVDBSensedObjectsProcessor
from src.core.data.sensed_object import SensedObject
from src.core.data.sensing_data import SensingData
from src.core.database.memory_kv_database import MemoryKVDatabase
from tests.unit.test_implementations.implementations import TestStaticSensor


class TestSensedObjectsProcessor:

    @fixture(autouse=True)
    def setUp(self):
        __database = MemoryKVDatabase()

        self.__static_objects_manager = Mock()
        self.__moving_objects_manager = Mock()
        self.__sensor_manager = Mock()
        self.__location_service = Mock()

        self.__test_sensor = TestStaticSensor(id="some_id", position="pos")

        self.__processor = KVDBSensedObjectsProcessor(database=__database,
                                                      static_objects_manager=self.__static_objects_manager,
                                                      moving_objects_manager=self.__moving_objects_manager,
                                                      sensors_manager=self.__sensor_manager,
                                                      location_service=self.__location_service)


    def test_sensor_information_is_added(self):
        sensed_object_id = "id"
        sensed_object_information = SensingData(distance=10, timestamp=1)

        sensor_id = "id"
        sensor = TestStaticSensor(id="some_id", position="pos")
        self.__sensor_manager.get_sensor.side_effect = (lambda sensor_id : sensor)

        self.__processor.process_new_data(sensor_id,{sensed_object_id: SensedObject(sensor=sensor, id=sensed_object_id, data=sensed_object_information)})

        assert len(sensor.get_sensed_objects()) == 1
        assert sensor.get_sensed_objects().get(sensed_object_id).data.distance == sensed_object_information.distance

    def test_sensor_information_is_removed(self):
        sensed_object_id = "id"
        sensed_object_information = SensingData(distance=10, timestamp=1)

        sensor_id = "id"
        self.__sensor_manager.get_sensor.side_effect = (lambda sensor_id: self.__test_sensor)

        self.__processor.process_new_data(sensor_id, {sensed_object_id: SensedObject(sensor=self.__test_sensor, id=sensed_object_id, data=sensed_object_information)})

        assert len(self.__test_sensor.get_sensed_objects()) == 1
        assert self.__test_sensor.get_sensed_objects().get(sensed_object_id).data.distance == sensed_object_information.distance

        sensed_object_id2 = "id2"
        sensed_object_information2 = SensingData(distance=20, timestamp=1)
        self.__processor.process_new_data(sensor_id, {sensed_object_id2: SensedObject(sensor=self.__test_sensor, id=sensed_object_id2, data=sensed_object_information2)})

        assert len(self.__test_sensor.get_sensed_objects()) == 1
        assert self.__test_sensor.get_sensed_objects().get(sensed_object_id2).data.distance ==sensed_object_information2.distance

    def test_sensor_information_is_updated(self):
        sensed_object_id = "id"
        sensed_object_information = SensingData(distance=20, timestamp=1)

        sensor_id = "id"
        self.__sensor_manager.get_sensor.side_effect = (lambda sensor_id: self.__test_sensor)

        self.__processor.process_new_data(sensor_id, {sensed_object_id: SensedObject(sensor=self.__test_sensor, id=sensed_object_id, data=sensed_object_information)})

        assert len(self.__test_sensor.get_sensed_objects()) == 1
        assert self.__test_sensor.get_sensed_objects().get(sensed_object_id).data.distance == sensed_object_information.distance

        sensed_object_information2 = SensingData(distance=20, timestamp=1)
        self.__processor.process_new_data(sensor_id, {sensed_object_id : SensedObject(sensor=self.__test_sensor, id=sensed_object_id, data=sensed_object_information2)})

        assert len(self.__test_sensor.get_sensed_objects()) == 1
        assert self.__test_sensor.get_sensed_objects().get(sensed_object_id).data.distance == sensed_object_information2.distance



