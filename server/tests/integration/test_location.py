from api import SENSORS_ENDPOINT, USERS_ENDPOINT, SIGNAL_EMITTERS_ENDPOINT, ANCHORS_ENDPOINT
from tests.integration.test_api import TestApi


class TestLocation(TestApi):

    def __add_user(self, user):
        assert self._client().post(USERS_ENDPOINT, json=user).status_code == 200

    def __add_anchor(self, anchor):
        assert self._client().post(ANCHORS_ENDPOINT, json=anchor).status_code == 200

    def __add_signal_emitter(self, signal_emitter):
        assert self._client().post(SIGNAL_EMITTERS_ENDPOINT, json=signal_emitter).status_code == 200

    def __update_sensor_in_user(self, user_id, sensor_id, data):
        endpoint = USERS_ENDPOINT + "/" + user_id + SENSORS_ENDPOINT + "/" + sensor_id
        assert self._client().put(endpoint, json=data).status_code == 200

    def __update_sensor_in_anchor(self, anchor_id, sensor_id, data):
        endpoint = ANCHORS_ENDPOINT + "/" + anchor_id + SENSORS_ENDPOINT + "/" + sensor_id
        assert self._client().put(endpoint, json=data).status_code == 200

    def __assert_location(self, actual_location, expected_location, allowed_error=0.001):
        assert abs(actual_location['x'] - expected_location[0]) < allowed_error
        assert abs(actual_location['y'] - expected_location[1]) < allowed_error

    def test_sensing_information_changes_location_on_emitter_user(self):
        #add static sensors
        static_sensor_id1 = "sensor1"
        static_sensor1 = {
            "id": static_sensor_id1
        }

        anchor1 = {
            "id" : "anchor1",
            "position" : {
                'x' : 0,
                'y' : 0,
            },
            "sensors" : {
                static_sensor_id1 : static_sensor1
            }
        }

        self.__add_anchor(anchor1)

        static_sensor_id2 = "sensor2"
        static_sensor2 = {
            "id": static_sensor_id2
        }

        anchor2 = {
            "id": "anchor2",
            "position": {
                'x': 10,
                'y': 0,
            },
            "sensors": {
                static_sensor_id2: static_sensor2
            }
        }

        self.__add_anchor(anchor2)

        moving_signal_emitter_id = "signal_emitter"
        moving_signal_emitter = {
            'id' : moving_signal_emitter_id
        }

        #add users
        user_id = "user"
        user = {
            "id": user_id,
            "position": {
                'x': 0,
                'y': 0
            },
            'signal_emitters' : {
                moving_signal_emitter_id : moving_signal_emitter
            }
        }

        self.__add_user(user)

        sensed_objects = [
                {
                    'id': moving_signal_emitter_id,
                    'data' : {
                        'distance' : 5,
                        'timestamp' : 1
                    }
                }
            ]
        #update sensor information and check that user position changed
        self.__update_sensor_in_anchor(anchor1['id'], static_sensor_id1, sensed_objects)

        sensed_objects = [
                {
                    'id': moving_signal_emitter_id,
                    'data': {
                        'distance': 5,
                        'timestamp': 2
                    }
                }
            ]

        self.__update_sensor_in_anchor(anchor2['id'], static_sensor_id2, sensed_objects)

        #get user and check position
        res = self._client().get(USERS_ENDPOINT + "/" + user_id)
        assert res.status_code == 200
        self.__assert_location(res.get_json()["position"], (5,0))

    def test_sensing_information_changes_location_on_sensing_user(self):
        # add static signal emitters
        emitter_id1 = "emitter1"
        anchor_id1 = "anchor1"
        anchor1 = {
            "id" : anchor_id1,
            "position": {
                'x':0,
                'y':0
            },
            "signal_emitters": {
                emitter_id1 : {
                    "id" : emitter_id1
                }
            }
        }

        self.__add_anchor(anchor1)

        emitter_id2 = "emitter2"
        anchor_id2 = "anchor2"
        anchor2 = {
            "id": anchor_id2,
            "position": {
                'x': 10,
                'y': 0
            },
            "signal_emitters": {
                emitter_id2: {
                    "id": emitter_id2
                }
            }
        }

        self.__add_anchor(anchor2)

        # add sensing user
        user_id = "user"
        sensor_id = "sensor"
        user = {
            "id" : user_id,
            "position" : {
                'x':0,
                'y':0
            },
            'sensors' : {
                sensor_id : {
                    'id' : sensor_id
                }
            }
        }
        self.__add_user(user)

        sensed_objects = [
                {
                    'id': emitter_id1,
                    'data': {
                        'distance': 5,
                        'timestamp': 1
                    }
                },
                {
                    'id': emitter_id2,
                    'data': {
                        'distance': 5,
                        'timestamp': 1
                    }
                }

            ]

        # update sensor information and check that user position changed
        self.__update_sensor_in_user(user_id, sensor_id, sensed_objects)

        # get user and check position
        res = self._client().get(USERS_ENDPOINT + "/" + user_id)
        assert res.status_code == 200
        self.__assert_location(res.get_json()["position"], (5, 0))

    def test_noise_in_sensed_information_static_sensor(self):
        anchor_id1 = "anchor1"
        sensor_id1 = "sensor1"
        anchor1 = {
            "id": anchor_id1,
            "position" : {
                'x': 0,
                'y': 0,
            },
            "sensors" : {
                sensor_id1: {
                    "id" : sensor_id1
                }
            }
        }

        self.__add_anchor(anchor1)

        anchor_id2 = "anchor2"
        sensor_id2 = "sensor2"
        anchor2 = {
            "id": anchor_id2,
            "position": {
                'x': 10,
                'y': 0,
            },
            "sensors": {
                sensor_id2: {
                    "id": sensor_id2
                }
            }
        }

        self.__add_anchor(anchor2)

        # add users
        user_id = "user"
        signal_emitter_id = "signal_emitter"
        user = {
            "id" : user_id,
            "position" : {
                'x' : 0,
                'y' : 0,
            },
            "signal_emitters" : {
                signal_emitter_id : {
                    'id' : signal_emitter_id
                }
            }
        }
        self.__add_user(user)

        sensed_objects = [
                {
                    'id': signal_emitter_id,
                    'data': {
                        'distance': 5,
                        'timestamp': 1
                    }
                }, {
                    'id': 'idontexist',
                    'data' : {
                        'distance': 1000,
                        'timestamp' :20
                    }
                }
            ]

        # update sensor information and check that user position changed
        self.__update_sensor_in_anchor(anchor_id1, sensor_id1, sensed_objects)

        sensed_objects = [
                {
                    'id': signal_emitter_id,
                    'data': {
                        'distance': 5,
                        'timestamp': 2
                    }
                }
            ]

        self.__update_sensor_in_anchor(anchor_id2, sensor_id2, sensed_objects)

        # get user and check position
        res = self._client().get(USERS_ENDPOINT + "/" + user_id)
        assert res.status_code == 200
        self.__assert_location(res.get_json()["position"], (5, 0))

    def test_sensing_information_changes_location_on_moving_sensor(self):
        # add static signal emitters

        emitter_id1 = "emitter1"
        anchor_id1 = "anchor1"
        anchor1 = {
            "id" : anchor_id1,
            "position" : {
                'x' : 0,
                'y' : 0
            },
            'signal_emitters' : {
                emitter_id1 : {
                    'id' : emitter_id1
                }
            }
        }

        self.__add_anchor(anchor1)

        emitter_id2 = "emitter2"
        anchor_id2 = "anchor2"
        anchor2 = {
            "id": anchor_id2,
            "position": {
                'x': 10,
                'y': 0
            },
            'signal_emitters': {
                emitter_id2: {
                    'id': emitter_id2
                }
            }
        }

        self.__add_anchor(anchor2)

        # add sensing user
        user_id = "user"
        sensor_id = "sensor"
        user = {
            "id" : user_id,
            "position" : {
                'x' : 0,
                'y' : 0
            },
            'sensors': {
                sensor_id : {
                    "id" : sensor_id
                }
            }
        }

        self.__add_user(user)

        sensed_objects = [
                {
                    'id': emitter_id1,
                    'data': {
                        'distance': 5,
                        'timestamp': 1
                    }
                },
                {
                    'id': emitter_id2,
                    'data': {
                        'distance': 5,
                        'timestamp': 1
                    }
                }, {
                    'id': 'noise',
                    'data' : {
                        'distance' : -1000000,
                        'timestamp': 45
                    }
                }

            ]

        # update sensor information and check that user position changed
        self.__update_sensor_in_user(user_id, sensor_id, sensed_objects)

        # get user and check position
        res = self._client().get(USERS_ENDPOINT + "/" + user_id)
        assert res.status_code == 200
        self.__assert_location(res.get_json()["position"], (5, 0))

    def test_less_than_required_sensing_points_still_returns_200(self):
        # add static signal emitters

        emitter_id = "emitter1"
        anchor_id = "anchor1"
        anchor = {
            "id": anchor_id,
            "position": {
                'x': 0,
                'y': 0
            },
            'signal_emitters': {
                emitter_id: {
                    'id': emitter_id
                }
            }
        }
        self.__add_anchor(anchor)

        # add sensing user
        user_id = "user"
        sensor_id = "sensor"
        user = {
            "id": user_id,
            "position": {
                'x': 0,
                'y': 0
            },
            'sensors': {
                sensor_id: {
                    "id": sensor_id
                }
            }
        }

        self.__add_user(user)

        sensed_objects = [
                {
                    'id': emitter_id,
                    'data': {
                        'distance': 5,
                        'timestamp': 1
                    }
                }
            ]

        # update sensor information and check that user position changed
        self.__update_sensor_in_user(user_id, sensor_id, sensed_objects)