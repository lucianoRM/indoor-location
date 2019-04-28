from src.core.anchor.sensing_anchor import SensingAnchor
from tests.unit.core.sensor.abstract_sensor_test import AbstractSensorTest


class TestSensingAnchor(AbstractSensorTest):

    def _create_sensor(self, id, position, name=None):
        return SensingAnchor(id=id, position=position, name=name)