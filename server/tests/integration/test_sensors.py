from api import SENSORS_ENDPOINT
from tests.integration.test_api import TestApi


class TestSensorsEndpoint(TestApi):

    def _do_set_up(self):
        self.__base_sensor = {
            "id": "sensorId",
            "position": {
                    'x':0,
                    'y':0
                },
            "type": "USER"
        }


    def test_get_empty_sensor_list(self):
        res = self._client().get(SENSORS_ENDPOINT)
        self.assert_response(res, [])

    def test_add_sensor_and_get_it(self):
        sensor = self.__base_sensor
        res = self._client().post(SENSORS_ENDPOINT, json=sensor)
        assert res.status_code == 200
        res = self._client().get(SENSORS_ENDPOINT + "/" + sensor['id'])
        self.assert_response(res, sensor, ['unit'])

    def test_add_sensor_twice_should_fail(self):
        sensor = self.__base_sensor
        res = self._client().post(SENSORS_ENDPOINT, json=sensor)
        assert res.status_code == 200
        res = self._client().post(SENSORS_ENDPOINT, json=sensor)
        assert res.status_code == 409
        assert "was already registered" in str(res.get_data())

    def test_add_multiple_sensors_and_get_list(self):
        sensors = [
            {
                "id": "sensorId",
                "position": {
                    'x':0,
                    'y':0
                },
                "type": "USER"
            },
            {
                "id": "sensorId2",
                "position": {
                    'x':0,
                    'y':0
                },
                "type": "ANCHOR"
            }
        ]
        for sensor in sensors:
            res = self._client().post(SENSORS_ENDPOINT, json=sensor)
            assert res.status_code == 200
        res = self._client().get(SENSORS_ENDPOINT)
        assert res.status_code == 200
        self.assert_response(res, sensors, ['unit'])
        
    def test_add_sensor_with_missing_id(self):
        sensor = self.__base_sensor
        sensor.pop("id")
        res = self._client().post(SENSORS_ENDPOINT, json=sensor)
        assert res.status_code == 400
        assert "Invalid format" in str(res.get_data())
        assert "id:Missing data for required field" in str(res.get_data())

    def test_add_sensor_with_missing_works_and_returns_default(self):
        sensor = self.__base_sensor
        sensor.pop("position")
        res = self._client().post(SENSORS_ENDPOINT, json=sensor)
        assert res.status_code == 200
        assert res.get_json()['position']['x'] == 0
        assert res.get_json()['position']['y'] == 0

    def test_add_sensor_with_missing_type(self):
        sensor = self.__base_sensor
        sensor.pop("type")
        res = self._client().post(SENSORS_ENDPOINT, json=sensor)
        assert res.status_code == 400
        assert "Missing type" in str(res.get_data())

    def test_add_sensor_with_wrong_type(self):
        sensor = self.__base_sensor
        sensor['type'] = "INVALID_TYPE"
        res = self._client().post(SENSORS_ENDPOINT, json=sensor)
        assert res.status_code == 400
        assert "Got wrong type: INVALID_TYPE, expecting one of" in str(res.get_data())
        assert "USER" in str(res.get_data())
        assert "ANCHOR" in str(res.get_data())