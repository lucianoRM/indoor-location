from pytest import fixture, raises

from src.core.object.sensor_aware_object import SensorAlreadyExistsException, UnknownSensorException
from src.core.object.signal_emitter_aware_object import SignalEmitterAlreadyExistsException, \
    UnknownSignalEmitterException
from src.core.user.user import User
from tests.unit.test_implementations.implementations import FakeSignalEmitter, FakeSensor


class TestUser:

    @fixture(autouse=True)
    def setUp(self):
        self.__test_user = User(
            id="id",
            name="name",
            position="position"
        )
        self.__test_sensor_id = 'id'
        self.__test_sensor = FakeSensor(id=self.__test_sensor_id, position=None)
        self.__test_se_id = 'seid'
        self.__test_se = FakeSignalEmitter(id=self.__test_se_id, position=None)

    def test_create_user_and_get_sensors(self):
        user = User(id="id",
                    name="name",
                    position="position",
                    sensors={
                        self.__test_sensor_id:self.__test_sensor
                    })

        assert user.sensors == {self.__test_sensor_id:self.__test_sensor}

    def test_create_user_and_get_se(self):
        user = User(id="id",
                    name="name",
                    position="position",
                    signal_emitters={
                        self.__test_se_id:self.__test_se
                    })

        assert user.signal_emitters == {self.__test_se_id:self.__test_se}

    def test_add_sensor(self):
        user = self.__test_user
        user.add_sensor(self.__test_sensor_id,self.__test_sensor)
        assert self.__test_sensor_id in user.sensors

    def test_add_se(self):
        user = self.__test_user
        user.add_signal_emitter(self.__test_se_id,self.__test_se)
        assert self.__test_se_id in user.signal_emitters

    def test_add_sensor_multiple_times(self):
        user = self.__test_user
        user.add_sensor(self.__test_sensor_id,self.__test_sensor)
        with raises(SensorAlreadyExistsException):
            user.add_sensor(self.__test_sensor_id, None)

    def test_add_se_multiple_times(self):
        user = self.__test_user
        user.add_signal_emitter(self.__test_se_id, self.__test_se)
        with raises(SignalEmitterAlreadyExistsException):
            user.add_signal_emitter(self.__test_se_id, None)

    def test_remove_sensor(self):
        user = self.__test_user
        user.add_sensor(self.__test_sensor_id, self.__test_sensor)
        assert self.__test_sensor_id in user.sensors
        user.remove_sensor(self.__test_sensor_id)
        assert self.__test_sensor_id not in user.sensors

    def test_remove_not_existent_sensor(self):
        user = self.__test_user
        with raises(UnknownSensorException):
            user.remove_sensor("s")

    def test_update_sensor(self):
        s_id = "s"
        s1 = FakeSensor(id=s_id, position="FIRST")
        user = self.__test_user
        user.add_sensor(s_id, s1)

        assert s_id in user.sensors

        s2 = FakeSensor(id=s_id, position="SECOND")
        user.update_sensor(s_id, s2)
        s = user.sensors.get(s_id)

        assert s == s2

    def test_update_not_existent_sensor(self):
        user = self.__test_user
        with raises(UnknownSensorException):
            user.update_sensor("s", "s")

    def test_remove_se(self):
        user = self.__test_user
        user.add_signal_emitter(self.__test_se_id, self.__test_se)
        assert self.__test_se_id in user.signal_emitters
        user.remove_signal_emitter(self.__test_se_id)
        assert self.__test_se_id not in user.signal_emitters

    def test_remove_not_existent_se(self):
        user = self.__test_user
        with raises(UnknownSignalEmitterException):
            user.remove_signal_emitter("s")

    def test_update_se(self):
        s_id = "s"
        s1 = FakeSignalEmitter(id=s_id, signal="FIRST")
        user = self.__test_user
        user.add_signal_emitter(s_id, s1)

        assert s_id in user.signal_emitters

        s2 = FakeSignalEmitter(id=s_id, signal="SECOND")
        user.update_signal_emitter(s_id, s2)
        s = user.signal_emitters.get(s_id)

        assert s == s2

    def test_update_not_existent_signal_emitter(self):
        user = self.__test_user
        with raises(UnknownSignalEmitterException):
            user.update_signal_emitter("s", "s")

    def test_get_se_has_user_position(self):
        user = self.__test_user
        se_id = "id"
        se_position = (99, 99)
        se = FakeSignalEmitter(id=se_id, position=se_position)
        user.add_signal_emitter(se_id, se)
        assert user.get_signal_emitter(se_id).position == user.position

    def test_se_position_changes_with_user_position(self):
        user = self.__test_user
        se_id = "id"
        se_position = (99, 99)
        se = FakeSignalEmitter(id=se_id, position=se_position)
        user.add_signal_emitter(se_id, se)
        assert user.get_signal_emitter(se_id).position == user.position
        new_position = (0,0)
        user.position = new_position
        assert user.get_signal_emitter(se_id).position == new_position

    def test_get_sensor_has_user_position(self):
        user = self.__test_user
        s_id = "id"
        s_position = (99, 99)
        s = FakeSensor(id=s_id, position=s_position)
        user.add_sensor(s_id, s)
        assert user.get_sensor(s_id).position == user.position

    def test_sensor_position_changes_with_user_position(self):
        user = self.__test_user
        s_id = "id"
        s_position = (99, 99)
        s = FakeSensor(id=s_id, position=s_position)
        user.add_sensor(s_id, s)
        assert user.get_sensor(s_id).position == user.position
        new_position = (0,0)
        user.position = new_position
        assert user.get_sensor(s_id).position == new_position