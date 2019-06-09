from pytest import raises

from tests.unit.test_implementations.implementations import FakeStaticObject


class TestStaticObjectUnitTest:

    def test_static_object_is_immutable(self):
        static_object = FakeStaticObject(id = None, position=None)
        with raises(AttributeError):
            static_object.position = 10