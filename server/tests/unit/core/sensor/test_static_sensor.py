from src.core.sensor.static_sensor import StaticSensor
from tests.unit.core.sensor.abstract_sensor_test import AbstractSensorTest


class TestStaticSensor(AbstractSensorTest):

    def _create_sensor(self, id, position, name=None):
        return StaticSensor(id=id, position=position, name=name)