from copy import deepcopy

from api import USERS_ENDPOINT, SENSORS_ENDPOINT, SIGNAL_EMITTERS_ENDPOINT
from tests.integration.test_api import TestApi


class TestUsersEndpoint(TestApi):

    def _do_set_up(self):
        self.__base_user = {
            "id": "userId",
            "position": {
                'x': 0.0,
                'y': 0.0
            }
        }

    def test_get_empty_user_list(self):
        res = self._client().get(USERS_ENDPOINT)
        self.assert_response(res, [])

    def test_get_not_existent_user(self):
        res = self._client().get(USERS_ENDPOINT + "/not_existent")
        assert res.status_code == 404
        assert "does not exist" in str(res.get_data())

    def test_add_user_and_get_it(self):
        user = self.__base_user
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        res = self._client().get(USERS_ENDPOINT + "/" + user['id'])
        self.assert_response(res, user)

    def test_add_minimal_user_and_get_it(self):
        user = self.__base_user
        user.pop('position')
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        res = self._client().get(USERS_ENDPOINT + "/" + user['id'])
        self.assert_response(res, user, 'position')

    def test_add_user_twice_should_fail(self):
        user = self.__base_user
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 409
        assert "was already registered" in str(res.get_data())

    def test_add_multiple_users_and_get_list(self):
        users = [
            {
                "id": "userId",
                "position": {
                    'x': 0,
                    'y': 0
                }
            },
            {
                "id": "userId2",
                "position": {
                    'x': 0,
                    'y': 0
                }
            }
        ]
        for user in users:
            res = self._client().post(USERS_ENDPOINT, json=user)
            assert res.status_code == 200
        res = self._client().get(USERS_ENDPOINT)
        assert res.status_code == 200
        self.assert_response(res, users)

    def test_add_user_with_sensors(self):
        user = self.__base_user
        s1_id = 's1'
        s1 = {'id': s1_id}
        s2_id = 's2'
        s2 = {'id': s1_id}
        user['sensors'] = {s1_id: s1, s2_id: s2}
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        self.assert_response(res, user, ['position'])

    def test_add_user_with_signal_emitters(self):
        user = self.__base_user
        se1_id = 'se1'
        se1 = {'id': se1_id}
        se2_id = 'se2'
        se2 = {'id': se1_id}
        user['signal_emitters'] = {se1_id: se1, se2_id: se2}
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        self.assert_response(res, user, ['position'])

    def test_add_user_with_sensors_and_signal_emitters(self):
        user = self.__base_user
        se_id = 'se'
        se = {'id': se_id}
        s_id = 's'
        s = {'id': s_id}
        user['sensors'] = {s_id: s}
        user['signal_emitters'] = {se_id: se}
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        self.assert_response(res, user, ['position'])

    def test_register_user_with_existent_sensor(self):
        user1 = self.__base_user
        s_id = 's'
        s = {'id': s_id}
        user1['sensors'] = {s_id: s}
        res = self._client().post(USERS_ENDPOINT, json=user1)
        assert res.status_code == 200

        user2 = {"id": "user2", 'sensors': {s_id: s}}
        res = self._client().post(USERS_ENDPOINT, json=user2)
        assert res.status_code == 409
        assert "The sensor with id: s already exists in the system" in str(res.get_data())

    def test_register_user_with_existent_signal_emitter(self):
        user1 = self.__base_user
        se_id = 'se'
        se = {'id': se_id}
        user1['signal_emitters'] = {se_id: se}
        res = self._client().post(USERS_ENDPOINT, json=user1)
        assert res.status_code == 200

        user2 = {"id": "user2", 'signal_emitters': {se_id: se}}
        res = self._client().post(USERS_ENDPOINT, json=user2)
        assert res.status_code == 409
        assert "The signal emitter with id: se already exists in the system" in str(res.get_data())

    def test_add_user_with_missing_id(self):
        user = self.__base_user
        user.pop("id")
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 400
        assert "Invalid format" in str(res.get_data())
        assert "id:Missing data for required field" in str(res.get_data())

    def test_add_user_with_missing_position_gets_default(self):
        user = self.__base_user
        user.pop("position")
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        assert res.get_json()['position']['x'] == 0
        assert res.get_json()['position']['y'] == 0

    def test_register_new_sensor_to_user(self):
        user = self.__base_user
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        sensor = {"id": "sensor_id"}
        res = self._client().post(USERS_ENDPOINT + "/" + user['id'] + "/sensors", json=sensor)
        assert res.status_code == 200
        res = self._client().get(SENSORS_ENDPOINT + "/" + sensor['id'])
        assert res.status_code == 200
        self.assert_response(res, sensor, ['position'])

    def test_register_new_sensor_to_user_multiple_times(self):
        user = self.__base_user
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        sensor = {"id": "sensor_id"}
        res = self._client().post(USERS_ENDPOINT + "/" + user['id'] + "/sensors", json=sensor)
        assert res.status_code == 200
        res = self._client().post(USERS_ENDPOINT + "/" + user['id'] + "/sensors", json=sensor)
        assert res.status_code == 409
        assert "The sensor with id: sensor_id already exists in the system" in str(res.get_data())

    def test_register_new_se_to_user(self):
        user = self.__base_user
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        se = {"id": "se_id"}
        res = self._client().post(USERS_ENDPOINT + "/" + user['id'] + "/signal_emitters", json=se)
        assert res.status_code == 200
        res = self._client().get(SIGNAL_EMITTERS_ENDPOINT + "/" + se['id'])
        assert res.status_code == 200
        self.assert_response(res, se, ['position'])

    def test_register_new_se_to_user_multiple_times(self):
        user = self.__base_user
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        se = {"id": "se_id"}
        res = self._client().post(USERS_ENDPOINT + "/" + user['id'] + "/signal_emitters", json=se)
        assert res.status_code == 200
        res = self._client().post(USERS_ENDPOINT + "/" + user['id'] + "/signal_emitters", json=se)
        assert res.status_code == 409
        assert "The signal emitter with id: se_id already exists in the system" in str(res.get_data())

    def test_update_not_existent_user(self):
        user = self.__base_user
        res = self._client().put(USERS_ENDPOINT + "/not_existent", json=user)
        assert res.status_code == 404
        assert "does not exist" in str(res.get_data())

    def test_update_user_and_get_it(self):
        user = self.__base_user
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        user['name'] = "new name"
        user['position'] = {
                'x': 10.0,
                'y': 10.0
            }
        res = self._client().put(USERS_ENDPOINT + "/" + user['id'], json=user)
        assert res.status_code == 200
        res = self._client().get(USERS_ENDPOINT + "/" + user['id'])
        self.assert_response(res, user)
