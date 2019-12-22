from unittest.mock import Mock
from pytest import fixture

from src.core.data.sensed_object import SensedObject
from src.core.data.sensing_data import SensingData
from src.core.data.sensing_user_objects_processor import SensingUserObjectsProcessor
from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.sensor.sensor import Sensor
from tests.unit.test_implementations.implementations import FakeUser

class TestSensedObjectsProcessor:

    @fixture(autouse=True)
    def setUp(self):
        __database = MemoryKVDatabase()


        self.__sensor_manager = Mock()
        self.__users_manager = Mock()
        self.__signal_emitters_manager = Mock()
        self.__location_service_provider = Mock()

        self.__test_sensor = Sensor(id="some_id", position=None)
        self.__test_user = FakeUser(id="fake_user", position=(0, 0))

        self.__processor = SensingUserObjectsProcessor(
            sensors_manager=self.__sensor_manager,
            users_manager=self.__users_manager,
            signal_emitters_manager=self.__signal_emitters_manager,
            location_service_provider=self.__location_service_provider
        )


    def test_sensor_information_is_added(self):
        sensed_object_id = "id"
        sensed_object_information = SensingData(distance=10, timestamp=1)

        sensor_id = "id"
        sensor = Sensor(id="some_id", position=None)
        self.__test_user.add_sensor(id=sensor_id, sensor=sensor)
        self.__users_manager.get_user.side_effect = (lambda user_id: self.__test_user)

        self.__processor.process_sensed_objects(self.__test_user.id,
                                                sensor_id,
                                                [SensedObject(id=sensed_object_id, data=sensed_object_information)])

        assert len(sensor.get_sensed_objects()) == 1
        assert sensor.get_sensed_objects().get(sensed_object_id).data.distance == sensed_object_information.distance

    def test_sensor_information_is_removed(self):
        sensed_object_id = "id"
        sensed_object_information = SensingData(distance=10, timestamp=1)

        sensor_id = "id"
        self.__users_manager.get_user.side_effect = (lambda user_id: self.__test_user)
        self.__test_user.add_sensor(id=sensor_id, sensor=self.__test_sensor)

        self.__processor.process_sensed_objects(self.__test_user.id,
                                                sensor_id,
                                                [SensedObject(id=sensed_object_id, data=sensed_object_information)])

        assert len(self.__test_sensor.get_sensed_objects()) == 1
        assert self.__test_sensor.get_sensed_objects().get(
            sensed_object_id).data.distance == sensed_object_information.distance

        sensed_object_id2 = "id2"
        sensed_object_information2 = SensingData(distance=20, timestamp=1)
        self.__processor.process_sensed_objects(self.__test_user.id,
                                                sensor_id,
                                                [SensedObject(id=sensed_object_id2, data=sensed_object_information2)])

        assert len(self.__test_sensor.get_sensed_objects()) == 1
        assert self.__test_sensor.get_sensed_objects().get(
            sensed_object_id2).data.distance == sensed_object_information2.distance

    def test_sensor_information_is_updated(self):
        sensed_object_id = "id"
        sensed_object_information = SensingData(distance=20, timestamp=1)

        sensor_id = "id"
        self.__users_manager.get_user.side_effect = (lambda user_id: self.__test_user)

        self.__test_user.add_sensor(id=sensor_id, sensor=self.__test_sensor)

        self.__processor.process_sensed_objects(self.__test_user.id,
                                                sensor_id,
                                                [SensedObject(id=sensed_object_id, data=sensed_object_information)])

        assert len(self.__test_sensor.get_sensed_objects()) == 1
        assert self.__test_sensor.get_sensed_objects().get(
            sensed_object_id).data.distance == sensed_object_information.distance

        sensed_object_information2 = SensingData(distance=20, timestamp=1)
        self.__processor.process_sensed_objects(self.__test_user.id,
                                                sensor_id,
                                                [SensedObject(id=sensed_object_id, data=sensed_object_information2)])

        assert len(self.__test_sensor.get_sensed_objects()) == 1
        assert self.__test_sensor.get_sensed_objects().get(
            sensed_object_id).data.distance == sensed_object_information2.distance

    def test_debugging_info_is_retrieved(self):
        sensed_object_id = "id"
        sensed_object_id2 = "id2"
        sensed_object_information = SensingData(distance=20, timestamp=1)

        sensor_id = "id"
        self.__users_manager.get_user.side_effect = (lambda user_id: self.__test_user)

        self.__test_user.add_sensor(id=sensor_id, sensor=self.__test_sensor)

        self.__processor.process_sensed_objects(self.__test_user.id,
                                                sensor_id,
                                                [SensedObject(id=sensed_object_id, data=sensed_object_information),
                                                 SensedObject(id=sensed_object_id2, data=sensed_object_information)])

        assert len(self.__test_sensor.get_sensed_objects()) == 2
        assert len(self.__test_user.attributes['sensed']) == 2
