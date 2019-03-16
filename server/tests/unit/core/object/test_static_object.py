from unittest import TestCase

from src.core.object.static_object import StaticObject


class StaticObjectUnitTest(TestCase):

    def test_static_object_is_immutable(self):
        static_object = StaticObject(id = None, position=None)
        try:
            static_object.position = 10
            self.fail("Should not allow setter")
        except AttributeError:
            #ok, it should fail
            pass