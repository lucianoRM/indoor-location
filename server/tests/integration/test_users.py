import json

from api import USERS_ENDPOINT
from tests.integration.test_api import TestApi


class TestUsersEndpoint(TestApi):

    def test_get_empty_user_list(self):
        res = self._client().get(USERS_ENDPOINT)
        self.assert_response(res, [])

    def test_add_user_and_get_it(self):
        user = {
            "id": "userId",
            "position": "position1"
        }
        res = self._client().post(USERS_ENDPOINT, json=json.dumps(user))
        assert res.status_code == 200
        res = self._client().get(USERS_ENDPOINT + "/" + user['id'])
        self.assert_response(res, user)

    def test_add_user_twice_should_fail(self):
        user = {
            "id": "userId",
            "position": "position1"
        }
        res = self._client().post(USERS_ENDPOINT, json=json.dumps(user))
        assert res.status_code == 200
        res = self._client().post(USERS_ENDPOINT, json=json.dumps(user))
        assert res.status_code == 500
        assert "was already registered" in str(res.get_data())

    def test_add_multiple_users_and_get_list(self):
        users = [
            {
                "id": "userId",
                "position": "position"
            },
            {
                "id": "userId2",
                "position": "position"
            }
        ]
        for user in users:
            res = self._client().post(USERS_ENDPOINT, json=json.dumps(user))
            assert res.status_code == 200
        res = self._client().get(USERS_ENDPOINT)
        assert res.status_code == 200
        self.assert_response(res, users)
