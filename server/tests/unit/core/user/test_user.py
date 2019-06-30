from pytest import fixture, raises

from src.core.object.sensor_aware_object import SensorAlreadyExistsException
from src.core.object.signal_emitter_aware_object import SignalEmitterAlreadyExistsException
from src.core.user.user import User


class TestUser:

    @fixture(autouse=True)
    def setUp(self):
        self.__test_user = User(
            id="id",
            name="name",
            position="position"
        )

    def test_create_user_and_get_sensors(self):
        user = User(id="id",
                    name="name",
                    position="position",
                    sensors={
                        "s": "SENSOR"
                    })

        assert user.sensors == {"s": "SENSOR"}

    def test_create_user_and_get_se(self):
        user = User(id="id",
                    name="name",
                    position="position",
                    signal_emitters={
                        "se": "SIGNAL_EMITTER"
                    })

        assert user.signal_emitters == {"se": "SIGNAL_EMITTER"}

    def test_add_sensor(self):
        user = self.__test_user
        user.add_sensor("s", "SENSOR")
        assert "s" in user.sensors

    def test_add_se(self):
        user = self.__test_user
        user.add_signal_emitter("se", "SIGNAL_EMITTER")
        assert "se" in user.signal_emitters

    def test_add_sensor_multiple_times(self):
        user = self.__test_user
        user.add_sensor("s", "SENSOR")
        with raises(SensorAlreadyExistsException):
            user.add_sensor("s", "SENSOR")

    def test_add_se_multiple_times(self):
        user = self.__test_user
        user.add_signal_emitter("se", "SIGNAL_EMTTER")
        with raises(SignalEmitterAlreadyExistsException):
            user.add_signal_emitter("se", "SIGNAL_EMITTER")