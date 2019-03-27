from unittest import TestCase

from src.core.sensor.static_sensor import StaticSensor
from tests.unit.core.sensor.test_sensor import SensorUnitTest


class StaticSensorUnitTest(SensorUnitTest, TestCase):

    def _create_sensor(self, id, position, name=None):
        return StaticSensor(id=id, position=position, name=name)