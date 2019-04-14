import json

from api import SENSORS_ENDPOINT, USERS_ENDPOINT
from tests.integration.test_api import TestApi


class TestLocation(TestApi):

    def __add_sensor(self, sensor):
        res = self._client().post(SENSORS_ENDPOINT, json=json.dumps(sensor))
        assert res.status_code == 200

    def __add_user(self, user):
        res = self._client().post(USERS_ENDPOINT, json=json.dumps(user))
        assert res.status_code == 200

    def __assert_location(self, actual_location, expected_location, allowed_error=0.001):
        assert abs(actual_location['x'] - expected_location[0]) < allowed_error
        assert abs(actual_location['y'] - expected_location[1]) < allowed_error


    def test_sensing_information_changes_location_on_emitter_user(self):
        #add static sensors

        sensor_id1 = "sensor1"
        self.__add_sensor({
            "id": sensor_id1,
            "position": {
                'x':0,
                'y':0
            },
            "type": "ANCHOR"
        })

        sensor_id2 = "sensor2"
        self.__add_sensor({
            "id": sensor_id2,
            "position": {
                    'x':10,
                    'y':0
                },
            "type": "ANCHOR"
        })

        #add users
        user_id = "user"
        self.__add_user({
            "id": user_id,
            "position": {
                    'x':0,
                    'y':0
                },
            "type": "SIGNAL_EMITTER"
        })

        #update sensor information and check that user position changed
        self._client().put(SENSORS_ENDPOINT + "/" + sensor_id1, json=json.dumps(
            {
                "sensed_objects" : {
                    "user" : {
                        "id": "user",
                        "sensed_data": {
                            "distance": {
                                "value" : 5,
                                "unit" : 'm'
                            },
                            "timestamp": 1
                        }
                    }
                }
            }
        ))
        self._client().put(SENSORS_ENDPOINT + "/" + sensor_id2, json=json.dumps(
            {
                "sensed_objects": {
                    "user": {
                        "id": "user",
                        "sensed_data": {
                            "distance": {
                                "value" : 5,
                                "unit" : 'm'
                            },
                            "timestamp": 2
                        }
                    }
                }
            }
        ))

        #get user and check position
        res = self._client().get(USERS_ENDPOINT + "/" + user_id)
        assert res.status_code == 200
        self.__assert_location(json.loads(res.get_json())["position"], (5,0))
