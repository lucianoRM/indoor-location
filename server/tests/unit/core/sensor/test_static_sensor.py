from src.core.sensor.static_sensor import StaticSensor
from tests.unit.core.sensor.test_sensor import SensorUnitTest


class TestStaticSensor(SensorUnitTest):

    def _create_sensor(self, id, position, name=None):
        return StaticSensor(id=id, position=position, name=name)