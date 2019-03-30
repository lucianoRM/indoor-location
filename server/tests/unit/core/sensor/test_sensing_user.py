from src.core.user.sensing_user import SensingUser
from tests.unit.core.sensor.abstract_sensor_test import AbstractSensorTest


class TestSensingUser(AbstractSensorTest):

    def _create_sensor(self, id, position, name=None):
        return SensingUser(id=id, position=position, name=name)