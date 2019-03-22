from unittest import TestCase

from src.core.data.sensed_object import SensedObject


class SensedObjectUnitTest(TestCase):

    def test_sensed_object_is_immutable(self):
        sensed_object = SensedObject(id= None, data= None, sensor=None)
        try:
            sensed_object.data = 10
            self.fail("Should not allow setter")
        except AttributeError:
            #ok, it should fail
            pass