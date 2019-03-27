from abc import ABCMeta, abstractmethod

from measurement.measures import Distance

from src.core.data.sensing_data import SensingData
from src.core.data.sensed_object import SensedObject


class SensorUnitTest(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def _create_sensor(self, id, position, name=None):
        pass


    def test_create_sensor_and_get_values(self):
        name = 'sensor1'
        id = 'sensorId'
        position = (5,5)
        sensor = self._create_sensor(id=id, position=position, name=name)
        self.assertEquals(sensor.name, name)
        self.assertEquals(sensor.id, id)
        self.assertEquals(sensor.position, position)


    def test_sensor_update_no_merge(self):
        sensor = self._create_sensor(id=1, position=1)

        sensed_object_id1 = "id1"
        sensed_distance1 = Distance(m=1)
        sensed_data1 = SensingData(distance=sensed_distance1, timestamp=1)
        sensed_object1 = SensedObject(id=sensed_object_id1, data=sensed_data1, sensor=None)

        sensor.update_sensed_objects({sensed_object_id1:sensed_object1})
        sensed_objects = sensor.get_sensed_objects()

        self.assertEquals(sensed_objects.get(sensed_object_id1).data.distance.m, sensed_distance1.m)

        sensed_object_id2 = "id2"
        sensed_distance2 = Distance(m=200)
        sensed_data2 = SensingData(distance=sensed_distance2, timestamp=1)
        sensed_object2 = SensedObject(id=sensed_object_id2, data=sensed_data2, sensor=None)

        sensor.update_sensed_objects({sensed_object_id2: sensed_object2})
        sensed_objects = sensor.get_sensed_objects()

        self.assertEquals(len(sensed_objects), 1)
        self.assertFalse(sensed_objects.has_key(sensed_object_id1))
        self.assertEquals(sensed_objects.get(sensed_object_id2).data.distance.m, sensed_distance2.m)


    def test_sensor_update_merge(self):
        sensor = self._create_sensor(id=1, position=1)

        sensed_object_id1 = "id1"
        sensed_distance1 = Distance(m=1)
        sensed_data1 = SensingData(distance=sensed_distance1, timestamp=1)
        sensed_object1 = SensedObject(id=sensed_object_id1, data=sensed_data1, sensor=None)

        sensor.update_sensed_objects({sensed_object_id1:sensed_object1})
        sensed_objects = sensor.get_sensed_objects()

        self.assertEquals(sensed_objects.get(sensed_object_id1).data.distance.m, sensed_distance1.m)

        sensed_object_id2 = "id2"
        sensed_distance2 = Distance(m=200)
        sensed_data2 = SensingData(distance=sensed_distance2, timestamp=1)
        sensed_object2 = SensedObject(id=sensed_object_id2, data=sensed_data2, sensor=None)

        sensor.update_sensed_objects({sensed_object_id2: sensed_object2}, merge=True)
        sensed_objects = sensor.get_sensed_objects()

        self.assertEquals(len(sensed_objects), 2)
        self.assertEquals(sensed_objects.get(sensed_object_id1).data.distance.m, sensed_distance1.m)
        self.assertEquals(sensed_objects.get(sensed_object_id2).data.distance.m, sensed_distance2.m)


    def test_sensor_update_merge_new_value(self):
        sensor = self._create_sensor(id=1, position=1)

        sensed_object_id1 = "id1"
        sensed_distance1a= Distance(m=1)
        sensed_data1a = SensingData(distance=sensed_distance1a, timestamp=1)
        sensed_object1 = SensedObject(id=sensed_object_id1, data=sensed_data1a, sensor=None)

        sensor.update_sensed_objects({sensed_object_id1:sensed_object1})
        sensed_objects = sensor.get_sensed_objects()

        self.assertEquals(sensed_objects.get(sensed_object_id1).data.distance.m, sensed_distance1a.m)

        sensed_distance1b = Distance(m=500)
        sensed_data1b = SensingData(distance=sensed_distance1b, timestamp=1)
        sensed_object1 = SensedObject(id=sensed_object_id1, data=sensed_data1b, sensor=None)
        sensed_object_id2 = "id2"
        sensed_distance2 = Distance(m=200)
        sensed_data2 = SensingData(distance=sensed_distance2, timestamp=1)
        sensed_object2 = SensedObject(id=sensed_object_id2, data=sensed_data2, sensor=None)

        sensor.update_sensed_objects(
            {sensed_object_id1:sensed_object1,
             sensed_object_id2: sensed_object2},
            merge=True)
        sensed_objects = sensor.get_sensed_objects()

        self.assertEquals(len(sensed_objects), 2)
        self.assertEquals(sensed_objects.get(sensed_object_id1).data.distance.m, sensed_distance1b.m)
        self.assertEquals(sensed_objects.get(sensed_object_id2).data.distance.m, sensed_distance2.m)