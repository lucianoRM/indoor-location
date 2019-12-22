
from tests.unit.test_implementations.implementations import FakeMovingObject


class TestMovingObjectUnitTest:

    def test_moving_object_has_position_setter(self):
        moving_object = FakeMovingObject(id = None, position=None)
        position = 10
        moving_object.position = position
        assert moving_object.position == position