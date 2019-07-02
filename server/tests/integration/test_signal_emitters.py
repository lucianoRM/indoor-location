from api import SIGNAL_EMITTERS_ENDPOINT, USERS_ENDPOINT, ANCHORS_ENDPOINT
from tests.integration.test_api import TestApi

class TestSignalEmittersEndpoint(TestApi):

    def _do_set_up(self):
        self.__base_user = {
            'id': 'userId'
        }
        self.__base_anchor = {
            'id': 'anchorId',
            'position': {
                'x': 0,
                'y': 0
            }
        }

        self.__base_signal_emitter_id = 'signal_emitter_id'
        self.__base_signal_emitter = {"id": self.__base_signal_emitter_id}

    def test_get_empty_signal_emitters_list(self):
        res = self._client().get(SIGNAL_EMITTERS_ENDPOINT)
        self.assert_response(res, [])

    def test_add_user_and_get_signal_emitter(self):
        user = self.__base_user
        user['signal_emitters'] = {self.__base_signal_emitter_id: self.__base_signal_emitter}
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        res = self._client().get(SIGNAL_EMITTERS_ENDPOINT + "/" + self.__base_signal_emitter_id)
        assert res.status_code == 200
        self.assert_response(res, self.__base_signal_emitter)

    def test_add_anchor_and_get_signal_emitter(self):
        anchor = self.__base_anchor
        anchor['signal_emitters'] = {self.__base_signal_emitter_id: self.__base_signal_emitter}
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200
        res = self._client().get(SIGNAL_EMITTERS_ENDPOINT + "/" + self.__base_signal_emitter_id)
        assert res.status_code == 200
        self.assert_response(res, self.__base_signal_emitter)

    # def test_add_signal_emitter_and_get_it(self):
    #     signal_emitter = self.__base_signal_emitter
    #     res = self._client().post(SIGNAL_EMITTERS_ENDPOINT, json=signal_emitter)
    #     assert res.status_code == 200
    #     res = self._client().get(SIGNAL_EMITTERS_ENDPOINT + "/" + signal_emitter['id'])
    #     self.assert_response(res, signal_emitter)
    # 
    # def test_add_signal_emitter_twice_should_fail(self):
    #     signal_emitter = self.__base_signal_emitter
    #     res = self._client().post(SIGNAL_EMITTERS_ENDPOINT, json=signal_emitter)
    #     assert res.status_code == 200
    #     res = self._client().post(SIGNAL_EMITTERS_ENDPOINT, json=signal_emitter)
    #     assert res.status_code == 409
    #     assert "was already registered" in str(res.get_data())
    # 
    # def test_add_multiple_signal_emitters_and_get_list(self):
    #     signal_emitters = [
    #         {
    #             "id": "signal_emitterId1",
    #             "signal": {
    #                 "a": "b"
    #             },
    #             "position": {
    #                 'x':0,
    #                 'y':0
    #             }
    #         },
    #         {
    #             "id": "signal_emitterId2",
    #             "signal": {
    #                 "a": "b"
    #             },
    #             "position": {
    #                 'x':0,
    #                 'y':0
    #             }
    #         }
    #     ]
    #     for signal_emitter in signal_emitters:
    #         res = self._client().post(SIGNAL_EMITTERS_ENDPOINT, json=signal_emitter)
    #         assert res.status_code == 200
    #     res = self._client().get(SIGNAL_EMITTERS_ENDPOINT)
    #     assert res.status_code == 200
    #     self.assert_response(res, signal_emitters)
    #     
    # def test_add_signal_emitter_with_missing_id(self):
    #     signal_emitter = self.__base_signal_emitter
    #     signal_emitter.pop("id")
    #     res = self._client().post(SIGNAL_EMITTERS_ENDPOINT, json=signal_emitter)
    #     assert res.status_code == 400
    #     assert "Invalid format" in str(res.get_data())
    #     assert "id:Missing data for required field" in str(res.get_data())
    # 
    # def test_add_signal_emitter_with_missing_position_gets_default(self):
    #     signal_emitter = self.__base_signal_emitter
    #     signal_emitter.pop("position")
    #     res = self._client().post(SIGNAL_EMITTERS_ENDPOINT, json=signal_emitter)
    #     assert res.status_code == 200
    #     assert res.get_json()['position']['x'] == 0
    #     assert res.get_json()['position']['y'] == 0