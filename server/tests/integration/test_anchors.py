from api import ANCHORS_ENDPOINT
from tests.integration.test_api import TestApi


class TestAnchorsEndpoint(TestApi):

    def _do_set_up(self):
        self.__base_anchor = {
            "id": "anchor_id",
            "position": {
                "x" : 0,
                "y" : 0
            },
            "type": "SENSOR"
        }

    def test_get_empty_anchor_list(self):
        res = self._client().get(ANCHORS_ENDPOINT)
        self.assert_response(res, [])

    def test_add_anchor_and_get_it(self):
        anchor = self.__base_anchor
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200
        res = self._client().get(ANCHORS_ENDPOINT + "/" + anchor['id'])
        self.assert_response(res, anchor, ['unit'])

    def test_add_anchor_twice_should_fail(self):
        user = self.__base_anchor
        res = self._client().post(ANCHORS_ENDPOINT, json=user)
        assert res.status_code == 200
        res = self._client().post(ANCHORS_ENDPOINT, json=user)
        assert res.status_code == 409
        assert "was already registered" in str(res.get_data())

    def test_add_multiple_anchors_and_get_list(self):
        anchors = [
            {
                "id": "anchor_id1",
                "position": {
                    'x':0,
                    'y':0
                },
                "type": "SENSOR"
            },
            {
                "id": "anchor_id2",
                "position": {
                    'x':0,
                    'y':0
                },
                "type": "SIGNAL_EMITTER",
                "signal": {"a":"a"}
            }
        ]
        for anchor in anchors:
            res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
            assert res.status_code == 200
        res = self._client().get(ANCHORS_ENDPOINT)
        assert res.status_code == 200
        self.assert_response(res, anchors, ['unit'])

    def test_add_anchor_with_missing_id(self):
        anchor = self.__base_anchor
        anchor.pop("id")
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 400
        assert "Missing id" in str(res.get_data())

    def test_add_anchor_with_missing_position(self):
        anchor = self.__base_anchor
        anchor.pop("position")
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 400
        assert "Missing position" in str(res.get_data())

    def test_add_anchor_with_missing_type(self):
        anchor = self.__base_anchor
        anchor.pop("type")
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 400
        assert "Missing type" in str(res.get_data())

    def test_add_anchor_with_wrong_type(self):
        anchor = self.__base_anchor
        anchor['type'] = "INVALID_TYPE"
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 400
        assert "Got wrong type: INVALID_TYPE, expecting one of: SENSOR, SIGNAL_EMITTER" in str(res.get_data())