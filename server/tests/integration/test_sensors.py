from api import SENSORS_ENDPOINT, USERS_ENDPOINT, ANCHORS_ENDPOINT
from tests.integration.test_api import TestApi


class TestSensorsEndpoint(TestApi):

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
        self.__base_sensor_id = 'sensorId'
        self.__base_sensor = {
            "id": self.__base_sensor_id
        }

    def test_get_empty_sensor_list(self):
        res = self._client().get(SENSORS_ENDPOINT)
        self.assert_response(res, [])

    def test_add_user_and_get_sensor(self):
        user = self.__base_user
        user['sensors'] = {self.__base_sensor_id: self.__base_sensor}
        res = self._client().post(USERS_ENDPOINT, json=user)
        assert res.status_code == 200
        res = self._client().get(SENSORS_ENDPOINT + "/" + self.__base_sensor_id)
        assert res.status_code == 200
        self.assert_response(res, self.__base_sensor)

    def test_add_anchor_and_get_sensor(self):
        anchor = self.__base_anchor
        anchor['sensors'] = {self.__base_sensor_id: self.__base_sensor}
        res = self._client().post(ANCHORS_ENDPOINT, json=anchor)
        assert res.status_code == 200
        res = self._client().get(SENSORS_ENDPOINT + "/" + self.__base_sensor_id)
        assert res.status_code == 200
        self.assert_response(res, self.__base_sensor)
    #
    # def test_add_sensor_twice_should_fail(self):
    #     sensor = self.__base_sensor
    #     res = self._client().post(SENSORS_ENDPOINT, json=sensor)
    #     assert res.status_code == 200
    #     res = self._client().post(SENSORS_ENDPOINT, json=sensor)
    #     assert res.status_code == 409
    #     assert "was already registered" in str(res.get_data())
    #
    # def test_add_multiple_sensors_and_get_list(self):
    #     sensors = [
    #         {
    #             "id": "sensorId",
    #             "position": {
    #                 'x': 0,
    #                 'y': 0
    #             }
    #         },
    #         {
    #             "id": "sensorId2",
    #             "position": {
    #                 'x': 0,
    #                 'y': 0
    #             }
    #         }
    #     ]
    #     for sensor in sensors:
    #         res = self._client().post(SENSORS_ENDPOINT, json=sensor)
    #         assert res.status_code == 200
    #     res = self._client().get(SENSORS_ENDPOINT)
    #     assert res.status_code == 200
    #     self.assert_response(res, sensors)
    #
    # def test_add_sensor_with_missing_id(self):
    #     sensor = self.__base_sensor
    #     sensor.pop("id")
    #     res = self._client().post(SENSORS_ENDPOINT, json=sensor)
    #     assert res.status_code == 400
    #     assert "Invalid format" in str(res.get_data())
    #     assert "id:Missing data for required field" in str(res.get_data())
    #
    # def test_add_sensor_with_missing_works_and_returns_default(self):
    #     sensor = self.__base_sensor
    #     sensor.pop("position")
    #     res = self._client().post(SENSORS_ENDPOINT, json=sensor)
    #     assert res.status_code == 200
    #     assert res.get_json()['position']['x'] == 0
    #     assert res.get_json()['position']['y'] == 0
