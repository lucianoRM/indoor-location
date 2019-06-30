from abc import ABCMeta, abstractmethod

from src.core.data.sensing_data import SensingData
from src.core.data.sensed_object import SensedObject

#Do not name this starting with Test so that the runner does not execute it
from src.core.sensor.sensor import Sensor


class TestSensor:


    def _create_sensor(self, id, name=None):
        return Sensor(id=id, name=name)


    def test_create_sensor_and_get_values(self):
        name = 'sensor1'
        id = 'sensorId'
        sensor = self._create_sensor(id=id, name=name)
        assert sensor.name == name
        assert sensor.id == id


    def test_sensor_update_no_merge(self):
        sensor = self._create_sensor(id=1)

        sensed_object_id1 = "id1"
        sensed_distance1 = 1
        sensed_data1 = SensingData(distance=sensed_distance1, timestamp=1)
        sensed_object1 = SensedObject(id=sensed_object_id1, data=sensed_data1,)

        sensor.update_sensed_objects([sensed_object1])
        sensed_objects = sensor.get_sensed_objects()

        assert sensed_objects.get(sensed_object_id1).data.distance == sensed_distance1

        sensed_object_id2 = "id2"
        sensed_distance2 = 200
        sensed_data2 = SensingData(distance=sensed_distance2, timestamp=1)
        sensed_object2 = SensedObject(id=sensed_object_id2, data=sensed_data2)

        sensor.update_sensed_objects([sensed_object2])
        sensed_objects = sensor.get_sensed_objects()

        assert len(sensed_objects) == 1
        assert sensed_object_id1 not in sensed_objects
        assert sensed_objects.get(sensed_object_id2).data.distance == sensed_distance2


    def test_sensor_update_merge(self):
        sensor = self._create_sensor(id=1)

        sensed_object_id1 = "id1"
        sensed_distance1 = 1
        sensed_data1 = SensingData(distance=sensed_distance1, timestamp=1)
        sensed_object1 = SensedObject(id=sensed_object_id1, data=sensed_data1)

        sensor.update_sensed_objects([sensed_object1])
        sensed_objects = sensor.get_sensed_objects()

        assert sensed_objects.get(sensed_object_id1).data.distance == sensed_distance1

        sensed_object_id2 = "id2"
        sensed_distance2 = 200
        sensed_data2 = SensingData(distance=sensed_distance2, timestamp=1)
        sensed_object2 = SensedObject(id=sensed_object_id2, data=sensed_data2)

        sensor.update_sensed_objects([sensed_object2], merge=True)
        sensed_objects = sensor.get_sensed_objects()

        assert len(sensed_objects) == 2
        assert sensed_objects.get(sensed_object_id1).data.distance == sensed_distance1
        assert sensed_objects.get(sensed_object_id2).data.distance == sensed_distance2


    def test_sensor_update_merge_new_value(self):
        sensor = self._create_sensor(id=1)

        sensed_object_id1 = "id1"
        sensed_distance1a= 1
        sensed_data1a = SensingData(distance=sensed_distance1a, timestamp=1)
        sensed_object1 = SensedObject(id=sensed_object_id1, data=sensed_data1a)

        sensor.update_sensed_objects([sensed_object1])
        sensed_objects = sensor.get_sensed_objects()

        assert sensed_objects.get(sensed_object_id1).data.distance == sensed_distance1a

        sensed_distance1b = 500
        sensed_data1b = SensingData(distance=sensed_distance1b, timestamp=1)
        sensed_object1 = SensedObject(id=sensed_object_id1, data=sensed_data1b)
        sensed_object_id2 = "id2"
        sensed_distance2 = 200
        sensed_data2 = SensingData(distance=sensed_distance2, timestamp=1)
        sensed_object2 = SensedObject(id=sensed_object_id2, data=sensed_data2)

        sensor.update_sensed_objects(
            [sensed_object1,sensed_object2],
            merge=True)
        sensed_objects = sensor.get_sensed_objects()

        assert len(sensed_objects) == 2
        assert sensed_objects.get(sensed_object_id1).data.distance == sensed_distance1b
        assert sensed_objects.get(sensed_object_id2).data.distance == sensed_distance2