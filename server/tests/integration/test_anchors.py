import json

from api import ANCHORS_ENDPOINT
from tests.integration.test_api import TestApi


class TestAnchorsEndpoint(TestApi):

    def _do_set_up(self):
        self.__base_anchor = {
            "id": "anchor_id",
            "position": "position1",
            "type": "SENSOR"
        }

    def test_get_empty_anchor_list(self):
        res = self._client().get(ANCHORS_ENDPOINT)
        self.assert_response(res, [])

    def test_add_anchor_and_get_it(self):
        anchor = self.__base_anchor
        res = self._client().post(ANCHORS_ENDPOINT, json=json.dumps(anchor))
        assert res.status_code == 200
        res = self._client().get(ANCHORS_ENDPOINT + "/" + anchor['id'])
        self.assert_response(res, anchor)

    def test_add_anchor_twice_should_fail(self):
        user = self.__base_anchor
        res = self._client().post(ANCHORS_ENDPOINT, json=json.dumps(user))
        assert res.status_code == 200
        res = self._client().post(ANCHORS_ENDPOINT, json=json.dumps(user))
        assert res.status_code == 500
        assert "was already registered" in str(res.get_data())

    def test_add_multiple_anchors_and_get_list(self):
        anchors = [
            {
                "id": "anchor_id1",
                "position": "position",
                "type": "SENSOR"
            },
            {
                "id": "anchor_id2",
                "position": "position",
                "type": "SIGNAL_EMITTER"
            }
        ]
        for anchor in anchors:
            res = self._client().post(ANCHORS_ENDPOINT, json=json.dumps(anchor))
            assert res.status_code == 200
        res = self._client().get(ANCHORS_ENDPOINT)
        assert res.status_code == 200
        self.assert_response(res, anchors)