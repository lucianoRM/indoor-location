from api import ANCHORS_ENDPOINT, SENSORS_ENDPOINT, SIGNAL_EMITTERS_ENDPOINT
from tests.integration.test_api import TestApi


class TestAnchorsEndpoint(TestApi):

    def _do_set_up(self):
        self.__base_anchor = {
            "id": "anchor_id",
            "position": {
                "x": 0,
                "y": 0
            }
        }

    def test_get_empty_anchor_list(self):
        res = self._client().get(ANCHORS_ENDPOINT)
        self.assert_response(res, [])

    def test_get_not_existent_anchor(self):
        res = self._client().get(ANCHORS_ENDPOINT + "/not_existent")
        assert res.status_code == 404
        assert "was never registered" in str(res.get_data())

    def test_add_anchor_and_get_it(self):
        anchor = self.__base_anchor
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200
        res = self._client().get(ANCHORS_ENDPOINT + "/" + anchor['id'])
        self.assert_response(res, anchor)

    def test_add_anchor_twice_should_fail(self):
        anchor = self.__base_anchor
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 409
        assert "was already registered" in str(res.get_data())

    def test_add_multiple_anchors_and_get_list(self):
        anchors = [
            {
                "id": "anchor_id1",
                "position": {
                    'x': 0,
                    'y': 0
                }
            },
            {
                "id": "anchor_id2",
                "position": {
                    'x': 0,
                    'y': 0
                }
            }
        ]
        for anchor in anchors:
            res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
            assert res.status_code == 200
        res = self._client().get(ANCHORS_ENDPOINT)
        assert res.status_code == 200
        self.assert_response(res, anchors)

    def test_add_anchor_with_sensors(self):
        anchor = self.__base_anchor
        s1_id = 's1'
        s1 = {'id': s1_id}
        s2_id = 's2'
        s2 = {'id': s1_id}
        anchor['sensors'] = {s1_id: s1, s2_id: s2}
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200
        self.assert_response(res, anchor, ['position'])

    def test_add_anchor_with_signal_emitters(self):
        anchor = self.__base_anchor
        se1_id = 'se1'
        se1 = {'id': se1_id}
        se2_id = 'se2'
        se2 = {'id': se1_id}
        anchor['signal_emitters'] = {se1_id: se1, se2_id: se2}
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200
        self.assert_response(res, anchor, ['position'])

    def test_add_anchor_with_sensors_and_signal_emitters(self):
        anchor = self.__base_anchor
        se_id = 'se'
        se = {'id': se_id}
        s_id = 's'
        s = {'id': s_id}
        anchor['sensors'] = {s_id: s}
        anchor['signal_emitters'] = {se_id: se}
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200
        self.assert_response(res, anchor, ['position'])

    def test_register_anchor_with_existent_sensor(self):
        anchor1 = self.__base_anchor
        s_id = 's'
        s = {'id': s_id}
        anchor1['sensors'] = {s_id: s}
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor1)
        assert res.status_code == 200

        anchor2 = {"id": "anchor2", 'position': {'x': 0, 'y': 0}, 'sensors': {s_id: s}}
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor2)
        assert res.status_code == 409
        assert "The sensor with id: s already exists in the system" in str(res.get_data())

    def test_register_anchor_with_existent_signal_emitter(self):
        anchor1 = self.__base_anchor
        se_id = 'se'
        se = {'id': se_id}
        anchor1['signal_emitters'] = {se_id: se}
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor1)
        assert res.status_code == 200

        anchor2 = {"id": "anchor2", 'position': {'x': 0, 'y': 0}, 'signal_emitters': {se_id: se}}
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor2)
        assert res.status_code == 409
        assert "The signal emitter with id: se already exists in the system" in str(res.get_data())

    def test_add_anchor_with_missing_id(self):
        anchor = self.__base_anchor
        anchor.pop("id")
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 400
        assert "Invalid format" in str(res.get_data())
        assert "id:Missing data for required field" in str(res.get_data())

    def test_add_anchor_with_missing_position(self):
        anchor = self.__base_anchor
        anchor.pop("position")
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert "Invalid format" in str(res.get_data())
        assert "position.x:Missing data for required field" in str(res.get_data())
        assert "position.y:Missing data for required field" in str(res.get_data())

    def test_register_new_sensor_to_anchor(self):
        anchor = self.__base_anchor
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200
        sensor = {"id" : "sensor_id"}
        res = self._client().post(ANCHORS_ENDPOINT + "/" + anchor['id'] + "/sensors", json=sensor)
        assert res.status_code == 200
        res = self._client().get(SENSORS_ENDPOINT + "/" + sensor['id'])
        assert res.status_code == 200
        self.assert_response(res, sensor,['position'])

    def test_register_new_sensor_to_anchor_multiple_times(self):
        anchor = self.__base_anchor
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200
        sensor = {"id" : "sensor_id"}
        res = self._client().post(ANCHORS_ENDPOINT + "/" + anchor['id'] + "/sensors", json=sensor)
        assert res.status_code == 200
        res = self._client().post(ANCHORS_ENDPOINT + "/" + anchor['id'] + "/sensors", json=sensor)
        assert res.status_code == 409
        assert "The sensor with id: sensor_id already exists in the system" in str(res.get_data())

    def test_register_new_se_to_anchor(self):
        anchor = self.__base_anchor
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200
        se = {"id" : "se_id"}
        res = self._client().post(ANCHORS_ENDPOINT + "/" + anchor['id'] + "/signal_emitters", json=se)
        assert res.status_code == 200
        res = self._client().get(SIGNAL_EMITTERS_ENDPOINT + "/" + se['id'])
        assert res.status_code == 200
        self.assert_response(res, se, ['position'])

    def test_register_new_se_to_anchor_multiple_times(self):
        anchor = self.__base_anchor
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200
        se = {"id" : "se_id"}
        res = self._client().post(ANCHORS_ENDPOINT + "/" + anchor['id'] + "/signal_emitters", json=se)
        assert res.status_code == 200
        res = self._client().post(ANCHORS_ENDPOINT + "/" + anchor['id'] + "/signal_emitters", json=se)
        assert res.status_code == 409
        assert "The signal emitter with id: se_id already exists in the system" in str(res.get_data())

    def test_delete_not_existent_anchor(self):
        anchor = self.__base_anchor
        res = self._client().delete(ANCHORS_ENDPOINT + "/" + anchor['id'])
        assert res.status_code == 404
        assert "No anchor with id" in str(res.get_data())

    def test_register_and_delete_twice(self):
        anchor = self.__base_anchor
        anchor = self.__base_anchor
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200  # register response
        res = self._client().delete(ANCHORS_ENDPOINT + "/" + anchor['id'])
        assert res.status_code == 200
        res = self._client().delete(ANCHORS_ENDPOINT + "/" + anchor['id'])
        assert res.status_code == 404
        assert "No anchor with id" in str(res.get_data())

    def test_register_and_delete_anchor(self):
        anchor = self.__base_anchor
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200 #register response
        res = self._client().get(ANCHORS_ENDPOINT + "/" + anchor['id'])
        assert res.status_code == 200 #check is in server

        se = {"id": "se_id"}
        res = self._client().post(ANCHORS_ENDPOINT + "/" + anchor['id'] + "/signal_emitters", json=se)
        assert res.status_code == 200 #register se
        res = self._client().get(SIGNAL_EMITTERS_ENDPOINT + "/" + se['id'])
        assert res.status_code == 200 #get se

        sensor = {"id": "sensor_id"}
        res = self._client().post(ANCHORS_ENDPOINT + "/" + anchor['id'] + "/sensors", json=sensor)
        assert res.status_code == 200 #register sensor
        res = self._client().get(SENSORS_ENDPOINT + "/" + sensor['id'])
        assert res.status_code == 200 #get sensor

        res = self._client().delete(ANCHORS_ENDPOINT + "/" + anchor['id'])
        assert res.status_code == 200 #delete anchor

        res = self._client().get(ANCHORS_ENDPOINT + "/" + anchor['id'])
        assert res.status_code == 404  #not in server

        res = self._client().get(SIGNAL_EMITTERS_ENDPOINT + "/" + se['id'])
        assert res.status_code == 404  #not in server

        res = self._client().get(SENSORS_ENDPOINT + "/" + sensor['id'])
        assert res.status_code == 404  #not in server


