from unittest import TestCase

from src.core.exception.exceptions import IllegalArgumentException
from src.core.sensor.sensor import Sensor, NAME_KEY, ID_KEY, LOCATION_KEY


class SensorUnitTest(TestCase):

    def test_create_sensor_and_get_values(self):
        name = 'sensor1'
        id = 'sensorId'
        location = (5,5)
        sensor = Sensor(**{NAME_KEY:name, ID_KEY:id, LOCATION_KEY:location})
        self.assertEquals(sensor.name, name)
        self.assertEquals(sensor.id, id)
        self.assertEquals(sensor.location, location)

    def test_sensor_creation_fails_if_missing_name(self):
        self.assertRaises(IllegalArgumentException, Sensor, **{ID_KEY:"someId", LOCATION_KEY : (0,0)})

    def test_sensor_creation_fails_if_missing_id(self):
        self.assertRaises(IllegalArgumentException, Sensor, **{NAME_KEY:"sensorName", LOCATION_KEY:(0,0)})

    def test_sensor_creation_fails_if_missing_location(self):
        self.assertRaises(IllegalArgumentException, Sensor, **{NAME_KEY : "sensorName" ,ID_KEY:"someId"})

    def test_sensor_equality(self):
        name1 = 'sensor1'
        id1 = 'sensorId'
        location1 = (5, 5)
        name2 = 'sensor1'
        id2 = 'sensorId'
        location2 = (5, 5)
        sensor1 = Sensor(**{NAME_KEY:name1, ID_KEY:id1, LOCATION_KEY:location1})
        sensor2 = Sensor(**{NAME_KEY:name2, ID_KEY:id2, LOCATION_KEY:location2})
        self.assertEquals(sensor1,sensor2)

    def test_sensor_inequality(self):
        name1 = 'sensor1'
        id1 = 'sensorId'
        location1 = (5, 5)
        sensor1 = Sensor(**{NAME_KEY:name1, ID_KEY:id1, LOCATION_KEY:location1})
        differentId = Sensor(**{NAME_KEY:name1, ID_KEY:"otherId", LOCATION_KEY:location1})
        self.assertNotEquals(sensor1,differentId)
        differentName = Sensor(**{NAME_KEY:"otherName", ID_KEY:id1, LOCATION_KEY:location1})
        self.assertNotEquals(sensor1,differentName)
        differentLocation = Sensor(**{NAME_KEY:name1, ID_KEY:id1, LOCATION_KEY:(10,10)})
        self.assertNotEquals(sensor1, differentLocation)