from pytest import fixture, raises

from src.core.anchor.anchor import Anchor
from src.core.object.sensor_aware_object import SensorAlreadyExistsException, UnknownSensorException
from src.core.object.signal_emitter_aware_object import SignalEmitterAlreadyExistsException, \
    UnknownSignalEmitterException


class TestAnchor:

    @fixture(autouse=True)
    def setUp(self):
        self.__test_anchor = Anchor(
            id="id",
            name="name",
            position="position"
        )

    def test_create_anchor_and_get_sensors(self):
        anchor = Anchor(id="id",
                        name="name",
                        position="position",
                        sensors={
                            "s": "SENSOR"
                        })

        assert anchor.sensors == {"s": "SENSOR"}

    def test_create_anchor_and_get_se(self):
        anchor = Anchor(id="id",
                        name="name",
                        position="position",
                        signal_emitters={
                            "se": "SIGNAL_EMITTER"
                        })

        assert anchor.signal_emitters == {"se": "SIGNAL_EMITTER"}

    def test_add_sensor(self):
        anchor = self.__test_anchor
        anchor.add_sensor("s", "SENSOR")
        assert "s" in anchor.sensors

    def test_add_se(self):
        anchor = self.__test_anchor
        anchor.add_signal_emitter("se", "SIGNAL_EMITTER")
        assert "se" in anchor.signal_emitters

    def test_add_sensor_multiple_times(self):
        anchor = self.__test_anchor
        anchor.add_sensor("s", "SENSOR")
        with raises(SensorAlreadyExistsException):
            anchor.add_sensor("s", "SENSOR")

    def test_add_se_multiple_times(self):
        anchor = self.__test_anchor
        anchor.add_signal_emitter("se", "SIGNAL_EMTTER")
        with raises(SignalEmitterAlreadyExistsException):
            anchor.add_signal_emitter("se", "SIGNAL_EMITTER")

    def test_remove_sensor(self):
        s_id = "s"
        anchor = self.__test_anchor
        anchor.add_sensor(s_id, "SENSOR")
        assert s_id in anchor.sensors
        anchor.remove_sensor(s_id)
        assert s_id not in anchor.sensors

    def test_remove_not_existent_sensor(self):
        anchor = self.__test_anchor
        with raises(UnknownSensorException):
            anchor.remove_sensor("s")

    def test_update_sensor(self):
        s_id = "s"
        s1 = "V1"
        anchor = self.__test_anchor
        anchor.add_sensor(s_id, s1)

        assert s_id in anchor.sensors

        s2 = "V2"
        anchor.update_sensor(s_id, s2)
        s = anchor.sensors.get(s_id)

        assert s == s2

    def test_update_not_existent_sensor(self):
        anchor = self.__test_anchor
        with raises(UnknownSensorException):
            anchor.update_sensor("s", "s")

    def test_remove_se(self):
        s_id = "s"
        anchor = self.__test_anchor
        anchor.add_signal_emitter(s_id, "SE")
        assert s_id in anchor.signal_emitters
        anchor.remove_signal_emitter(s_id)
        assert s_id not in anchor.signal_emitters

    def test_remove_not_existent_se(self):
        anchor = self.__test_anchor
        with raises(UnknownSignalEmitterException):
            anchor.remove_signal_emitter("s")

    def test_update_se(self):
        s_id = "s"
        s1 = "V1"
        anchor = self.__test_anchor
        anchor.add_signal_emitter(s_id, s1)

        assert s_id in anchor.signal_emitters

        s2 = "V2"
        anchor.update_signal_emitter(s_id, s2)
        s = anchor.signal_emitters.get(s_id)

        assert s == s2

    def test_update_not_existent_signal_emitter(self):
        anchor = self.__test_anchor
        with raises(UnknownSignalEmitterException):
            anchor.update_signal_emitter("s", "s")
