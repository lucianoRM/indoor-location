import pytest

from src.core.data.sensed_object import SensedObject


class TestSensedObject:

    def test_sensed_object_is_immutable(self):
        sensed_object = SensedObject(id= None, data= None, sensor=None)
        with pytest.raises(AttributeError):
            sensed_object.data = 10
