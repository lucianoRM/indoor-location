from unittest import TestCase

from src.core.object.moving_object import MovingObject
from tests.unit.test_implementations.implementations import TestMovingObject


class MovingObjectUnitTest(TestCase):

    def test_moving_object_has_position_setter(self):
        moving_object = TestMovingObject(id = None, position=None)
        position = 10
        moving_object.position = position
        self.assertEquals(moving_object.position, position)