from unittest import TestCase

from src.core.object.moving_object import MovingObject


class MovingObjectUnitTest(TestCase):

    def test_moving_object_has_position_setter(self):
        moving_object = MovingObject(id = None, position=None)
        position = 10
        moving_object.position = position
        self.assertEquals(moving_object.position, position)