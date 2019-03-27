from unittest import TestCase

from src.core.object.static_object import StaticObject
from tests.unit.test_implementations.implementations import TestStaticObject


class StaticObjectUnitTest(TestCase):

    def test_static_object_is_immutable(self):
        static_object = TestStaticObject(id = None, position=None)
        try:
            static_object.position = 10
            self.fail("Should not allow setter")
        except AttributeError:
            #ok, it should fail
            pass