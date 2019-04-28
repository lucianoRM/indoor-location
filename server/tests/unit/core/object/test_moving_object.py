
from tests.unit.test_implementations.implementations import TestMovingObject


class TestMovingObjectUnitTest:

    def test_moving_object_has_position_setter(self):
        moving_object = TestMovingObject(id = None, position=None)
        position = 10
        moving_object.position = position
        assert moving_object.position == position