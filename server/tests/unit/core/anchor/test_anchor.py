from pytest import fixture, raises

from src.core.anchor.anchor import Anchor
from src.core.object.sensor_aware_object import SensorAlreadyExistsException, UnknownSensorException
from src.core.object.signal_emitter_aware_object import SignalEmitterAlreadyExistsException, \
    UnknownSignalEmitterException
from src.resources.schemas.anchor_schema import AnchorSchema
from src.resources.schemas.serializer import Serializer
from tests.unit.test_implementations.implementations import FakeSignalEmitter, FakeSensor


class TestAnchor:

    @fixture(autouse=True)
    def setUp(self):
        self.__test_anchor = Anchor(
            id="id",
            name="name",
            position="position"
        )
        self.__test_sensor_id = 'sid'
        self.__test_sensor = FakeSensor(id=self.__test_sensor_id, position=None)
        self.__test_se_id = 'seid'
        self.__test_se = FakeSignalEmitter(id=self.__test_se_id, position=None)

    def test_create_anchor_and_get_sensors(self):
        anchor = Anchor(id="id",
                        name="name",
                        position="position",
                        sensors={
                            self.__test_sensor_id: self.__test_sensor
                        })

        assert anchor.sensors == {self.__test_sensor_id: self.__test_sensor}

    def test_create_anchor_and_get_se(self):
        anchor = Anchor(id="id",
                        name="name",
                        position="position",
                        signal_emitters={
                            self.__test_se_id:self.__test_se
                        })

        assert anchor.signal_emitters == {self.__test_se_id:self.__test_se}

    def test_add_sensor(self):
        anchor = self.__test_anchor
        anchor.add_sensor(self.__test_sensor_id, self.__test_sensor)
        assert self.__test_sensor_id in anchor.sensors

    def test_add_se(self):
        anchor = self.__test_anchor
        anchor.add_signal_emitter(self.__test_se_id, self.__test_se)
        assert self.__test_se_id in anchor.signal_emitters

    def test_add_sensor_multiple_times(self):
        anchor = self.__test_anchor
        anchor.add_sensor(self.__test_sensor_id, self.__test_sensor)
        with raises(SensorAlreadyExistsException):
            anchor.add_sensor(self.__test_sensor_id, None)

    def test_add_se_multiple_times(self):
        anchor = self.__test_anchor
        anchor.add_signal_emitter(self.__test_se_id, self.__test_se)
        with raises(SignalEmitterAlreadyExistsException):
            anchor.add_signal_emitter(self.__test_se_id, None)

    def test_remove_sensor(self):
        anchor = self.__test_anchor
        anchor.add_sensor(self.__test_sensor_id, self.__test_sensor)
        assert self.__test_sensor_id in anchor.sensors
        anchor.remove_sensor(self.__test_sensor_id)
        assert self.__test_sensor_id not in anchor.sensors

    def test_remove_not_existent_sensor(self):
        anchor = self.__test_anchor
        with raises(UnknownSensorException):
            anchor.remove_sensor("s")

    def test_update_sensor(self):
        s_id = "s"
        s1 = FakeSensor(id=s_id)
        anchor = self.__test_anchor
        anchor.add_sensor(s_id, s1)

        assert s_id in anchor.sensors

        s2 = FakeSensor(id=s_id, position="OTHER POSITION")
        anchor.update_sensor(s_id, s2)
        s = anchor.sensors.get(s_id)

        assert s == s2

    def test_update_not_existent_sensor(self):
        anchor = self.__test_anchor
        with raises(UnknownSensorException):
            anchor.update_sensor("s", "s")

    def test_remove_se(self):
        anchor = self.__test_anchor
        anchor.add_signal_emitter(self.__test_se_id, self.__test_se)
        assert self.__test_se_id in anchor.signal_emitters
        anchor.remove_signal_emitter(self.__test_se_id)
        assert self.__test_se_id not in anchor.signal_emitters

    def test_remove_not_existent_se(self):
        anchor = self.__test_anchor
        with raises(UnknownSignalEmitterException):
            anchor.remove_signal_emitter("s")

    def test_update_se(self):
        s_id = "s"
        s1 = FakeSignalEmitter(id=s_id, signal="SOME SIGNAL")
        anchor = self.__test_anchor
        anchor.add_signal_emitter(s_id, s1)

        assert s_id in anchor.signal_emitters

        s2 = FakeSignalEmitter(id=s_id, signal="OTHER SIGNAL")
        anchor.update_signal_emitter(s_id, s2)
        s = anchor.signal_emitters.get(s_id)

        assert s == s2

    def test_update_not_existent_signal_emitter(self):
        anchor = self.__test_anchor
        with raises(UnknownSignalEmitterException):
            anchor.update_signal_emitter("s", "s")

    def test_get_se_has_anchor_position(self):
        anchor = self.__test_anchor
        se_id = "id"
        se_position = (99, 99)
        se = FakeSignalEmitter(id=se_id, position=se_position)
        anchor.add_signal_emitter(se_id, se)
        assert anchor.get_signal_emitter(se_id).position == anchor.position

    def test_get_sensor_has_anchor_position(self):
        anchor = self.__test_anchor
        s_id = "id"
        s_position = (99, 99)
        s = FakeSensor(id=s_id, position=s_position)
        anchor.add_sensor(s_id, s)
        assert anchor.get_sensor(s_id).position == anchor.position