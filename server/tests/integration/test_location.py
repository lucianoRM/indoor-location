from api import SENSORS_ENDPOINT, USERS_ENDPOINT, SIGNAL_EMITTERS_ENDPOINT
from tests.integration.test_api import TestApi


class TestLocation(TestApi):

    def __add_sensor(self, sensor):
        assert self._client().post(SENSORS_ENDPOINT, json=sensor).status_code == 200

    def __add_user(self, user):
        assert self._client().post(USERS_ENDPOINT, json=user).status_code == 200

    def __add_signal_emitter(self, signal_emitter):
        assert self._client().post(SIGNAL_EMITTERS_ENDPOINT, json=signal_emitter).status_code == 200

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

        sensors = [
                {
                    'id': 'user',
                    'data' : {
                        'distance' : {
                            'value' : 5,
                            'unit' : 'm'
                        },
                        'timestamp' : 1
                    }
                }
            ]
        #update sensor information and check that user position changed
        self._client().put(SENSORS_ENDPOINT + "/" + sensor_id1, json=sensors)

        sensed_objects = [
                {
                    'id': 'user',
                    'data': {
                        'distance': {
                            'value': 5,
                            'unit': 'm'
                        },
                        'timestamp': 2
                    }
                }
            ]

        self._client().put(SENSORS_ENDPOINT + "/" + sensor_id2, json=sensed_objects)

        #get user and check position
        res = self._client().get(USERS_ENDPOINT + "/" + user_id)
        assert res.status_code == 200
        self.__assert_location(res.get_json()["position"], (5,0))

    def test_sensing_information_changes_location_on_sensing_user(self):
        # add static signal emitters

        emitter_id1 = "emitter1"
        self.__add_signal_emitter({
            "id": emitter_id1,
            "position": {
                'x': 0,
                'y': 0
            },
            "type": "ANCHOR"
        })

        emitter_id2 = "emitter2"
        self.__add_signal_emitter({
            "id": emitter_id2,
            "position": {
                'x': 10,
                'y': 0
            },
            "type": "ANCHOR"
        })

        # add sensing user
        user_id = "user"
        self.__add_user({
            "id": user_id,
            "position": {
                'x': 0,
                'y': 0
            },
            "type": "SENSOR"
        })

        sensed_objects = [
                {
                    'id': emitter_id1,
                    'data': {
                        'distance': {
                            'value': 5,
                            'unit': 'm'
                        },
                        'timestamp': 1
                    }
                },
                {
                    'id': emitter_id2,
                    'data': {
                        'distance': {
                            'value': 5,
                            'unit': 'm'
                        },
                        'timestamp': 1
                    }
                }

            ]

        # update sensor information and check that user position changed
        self._client().put(SENSORS_ENDPOINT + "/" + user_id, json=sensed_objects)

        # get user and check position
        res = self._client().get(USERS_ENDPOINT + "/" + user_id)
        assert res.status_code == 200
        self.__assert_location(res.get_json()["position"], (5, 0))

    def test_noise_in_sensed_information_static_sensor(self):
        sensor_id1 = "sensor1"
        self.__add_sensor({
            "id": sensor_id1,
            "position": {
                'x': 0,
                'y': 0
            },
            "type": "ANCHOR"
        })

        sensor_id2 = "sensor2"
        self.__add_sensor({
            "id": sensor_id2,
            "position": {
                'x': 10,
                'y': 0
            },
            "type": "ANCHOR"
        })

        # add users
        user_id = "user"
        self.__add_user({
            "id": user_id,
            "position": {
                'x': 0,
                'y': 0
            },
            "type": "SIGNAL_EMITTER"
        })

        sensors = [
                {
                    'id': 'user',
                    'data': {
                        'distance': {
                            'value': 5,
                            'unit': 'm'
                        },
                        'timestamp': 1
                    }
                }, {
                    'id': 'idontexist',
                    'data' : {
                        'distance': {
                            'value' : 1000,
                            'unit' : 'm'
                        },
                        'timestamp' :20
                    }
                }
            ]

        # update sensor information and check that user position changed
        self._client().put(SENSORS_ENDPOINT + "/" + sensor_id1, json=sensors)

        sensed_objects = [
                {
                    'id': 'user',
                    'data': {
                        'distance': {
                            'value': 5,
                            'unit': 'm'
                        },
                        'timestamp': 2
                    }
                }
            ]

        self._client().put(SENSORS_ENDPOINT + "/" + sensor_id2, json=sensed_objects)

        # get user and check position
        res = self._client().get(USERS_ENDPOINT + "/" + user_id)
        assert res.status_code == 200
        self.__assert_location(res.get_json()["position"], (5, 0))

    def test_sensing_information_changes_location_on_moving_sensor(self):
        # add static signal emitters

        emitter_id1 = "emitter1"
        self.__add_signal_emitter({
            "id": emitter_id1,
            "position": {
                'x': 0,
                'y': 0
            },
            "type": "ANCHOR"
        })

        emitter_id2 = "emitter2"
        self.__add_signal_emitter({
            "id": emitter_id2,
            "position": {
                'x': 10,
                'y': 0
            },
            "type": "ANCHOR"
        })

        # add sensing user
        user_id = "user"
        self.__add_user({
            "id": user_id,
            "position": {
                'x': 0,
                'y': 0
            },
            "type": "SENSOR"
        })

        sensed_objects = [
                {
                    'id': emitter_id1,
                    'data': {
                        'distance': {
                            'value': 5,
                            'unit': 'm'
                        },
                        'timestamp': 1
                    }
                },
                {
                    'id': emitter_id2,
                    'data': {
                        'distance': {
                            'value': 5,
                            'unit': 'm'
                        },
                        'timestamp': 1
                    }
                }, {
                    'id': 'noise',
                    'data' : {
                        'distance' : {
                            'value' : -1000,
                            'unit': 'km'
                        },
                        'timestamp': 45
                    }
                }

            ]

        # update sensor information and check that user position changed
        self._client().put(SENSORS_ENDPOINT + "/" + user_id, json=sensed_objects)

        # get user and check position
        res = self._client().get(USERS_ENDPOINT + "/" + user_id)
        assert res.status_code == 200
        self.__assert_location(res.get_json()["position"], (5, 0))

    def test_less_than_required_sensing_points_still_returns_200(self):
        # add static signal emitters

        emitter_id1 = "emitter1"
        self.__add_signal_emitter({
            "id": emitter_id1,
            "position": {
                'x': 0,
                'y': 0
            },
            "type": "ANCHOR"
        })

        # add sensing user
        user_id = "user"
        self.__add_user({
            "id": user_id,
            "position": {
                'x': 0,
                'y': 0
            },
            "type": "SENSOR"
        })

        sensed_objects = [
                {
                    'id': emitter_id1,
                    'data': {
                        'distance': {
                            'value': 5,
                            'unit': 'm'
                        },
                        'timestamp': 1
                    }
                }
            ]

        # update sensor information and check that user position changed
        res = self._client().put(SENSORS_ENDPOINT + "/" + user_id, json=sensed_objects)
        assert res.status_code == 200

