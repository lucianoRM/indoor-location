from api import USERS_ENDPOINT
from tests.integration.test_api import TestApi


class TestUsersEndpoint(TestApi):

    def _do_set_up(self):
        self.__base_user = {
            "id": "userId",
            "position": {
                    'x':0,
                    'y':0
                },
            "type": "SENSOR"
        }

    def test_get_empty_user_list(self):
        res = self._client().get(USERS_ENDPOINT)
        self.assert_response(res, [])

    def test_add_user_and_get_it(self):
        user = self.__base_user
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        res = self._client().get(USERS_ENDPOINT + "/" + user['id'])
        self.assert_response(res, user)

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
                    'x':0,
                    'y':0
                },
                "type": "SENSOR"
            },
            {
                "id": "userId2",
                "position": {
                    'x':0,
                    'y':0
                },
                "type": "SIGNAL_EMITTER"
            }
        ]
        for user in users:
            res = self._client().post(USERS_ENDPOINT, json=user)
            assert res.status_code == 200
        res = self._client().get(USERS_ENDPOINT)
        assert res.status_code == 200
        self.assert_response(res, users)

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

    def test_add_user_with_missing_type(self):
        user = self.__base_user
        user.pop("type")
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 400
        assert "Missing type" in str(res.get_data())

    def test_add_user_with_wrong_type(self):
        user = self.__base_user
        user['type'] = "INVALID_TYPE"
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 400
        assert "Got wrong type: INVALID_TYPE, expecting one of: SENSOR, SIGNAL_EMITTER" in str(res.get_data())
