import json

from api import SENSORS_ENDPOINT
from tests.integration.test_api import ApiTestCase


class SensorsEndpointTestCase(ApiTestCase):

    def test_get_empty_sensor_list(self):
        res = self._client().get(SENSORS_ENDPOINT)
        self.assert_response(res, [])

    def test_add_sensor_and_get_it(self):
        sensor = {
            "id": "sensorId",
            "position": "position1"
        }
        res = self._client().post(SENSORS_ENDPOINT, json=json.dumps(sensor))
        self.assertEquals(res.status_code, 200)
        res = self._client().get(SENSORS_ENDPOINT + "/" + sensor['id'])
        self.assert_response(res, sensor)

    def test_add_sensor_twice_should_fail(self):
        sensor = {
            "id": "sensorId",
            "position": "position1"
        }
        res = self._client().post(SENSORS_ENDPOINT, json=json.dumps(sensor))
        self.assertEquals(res.status_code, 200)
        res = self._client().post(SENSORS_ENDPOINT, json=json.dumps(sensor))
        self.assertEquals(res.status_code, 500)
        self.assertTrue("was already registered" in res.get_data())

    def test_add_multiple_sensors_and_get_list(self):
        sensors = [
            {
                "id": "sensorId",
                "position": "position"
            },
            {
                "id": "sensorId2",
                "position": "position"
            }
        ]
        for sensor in sensors:
            res = self._client().post(SENSORS_ENDPOINT, json=json.dumps(sensor))
            self.assertEquals(res.status_code, 200)
        res = self._client().get(SENSORS_ENDPOINT)
        self.assertEquals(res.status_code, 200)
        self.assert_response(res, sensors)