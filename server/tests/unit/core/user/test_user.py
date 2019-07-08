from pytest import fixture, raises

from src.core.object.sensor_aware_object import SensorAlreadyExistsException, UnknownSensorException
from src.core.object.signal_emitter_aware_object import SignalEmitterAlreadyExistsException, \
    UnknownSignalEmitterException
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

    def test_remove_sensor(self):
        s_id = "s"
        user = self.__test_user
        user.add_sensor(s_id, "SENSOR")
        assert s_id in user.sensors
        user.remove_sensor(s_id)
        assert s_id not in user.sensors

    def test_remove_not_existent_sensor(self):
        user = self.__test_user
        with raises(UnknownSensorException):
            user.remove_sensor("s")

    def test_update_sensor(self):
        s_id = "s"
        s1 = "V1"
        user = self.__test_user
        user.add_sensor(s_id, s1)

        assert s_id in user.sensors

        s2 = "V2"
        user.update_sensor(s_id, s2)
        s = user.sensors.get(s_id)

        assert s == s2

    def test_update_not_existent_sensor(self):
        user = self.__test_user
        with raises(UnknownSensorException):
            user.update_sensor("s", "s")

    def test_remove_se(self):
        s_id = "s"
        user = self.__test_user
        user.add_signal_emitter(s_id, "SE")
        assert s_id in user.signal_emitters
        user.remove_signal_emitter(s_id)
        assert s_id not in user.signal_emitters

    def test_remove_not_existent_se(self):
        user = self.__test_user
        with raises(UnknownSignalEmitterException):
            user.remove_signal_emitter("s")

    def test_update_se(self):
        s_id = "s"
        s1 = "V1"
        user = self.__test_user
        user.add_signal_emitter(s_id, s1)

        assert s_id in user.signal_emitters

        s2 = "V2"
        user.update_signal_emitter(s_id, s2)
        s = user.signal_emitters.get(s_id)

        assert s == s2

    def test_update_not_existent_signal_emitter(self):
        user = self.__test_user
        with raises(UnknownSignalEmitterException):
            user.update_signal_emitter("s", "s")