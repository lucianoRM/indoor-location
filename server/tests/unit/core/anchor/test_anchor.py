from pytest import fixture, raises

from src.core.anchor.anchor import Anchor
from src.core.object.sensor_aware_object import SensorAlreadyExistsException
from src.core.object.signal_emitter_aware_object import SignalEmitterAlreadyExistsException

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