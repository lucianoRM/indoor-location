from unittest import TestCase

from src.core.user.sensing_user import SensingUser
from tests.unit.core.sensor.test_sensor import SensorUnitTest


class SensingUserUnitTest(SensorUnitTest, TestCase):

    def _create_sensor(self, id, position, name=None):
        return SensingUser(id=id, position=position, name=name)