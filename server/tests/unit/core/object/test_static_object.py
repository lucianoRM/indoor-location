from pytest import raises

from tests.unit.test_implementations.implementations import TestStaticObject


class TestStaticObjectUnitTest:

    def test_static_object_is_immutable(self):
        static_object = TestStaticObject(id = None, position=None)
        with raises(AttributeError):
            static_object.position = 10