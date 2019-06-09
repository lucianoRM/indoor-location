from abc import ABCMeta
from copy import deepcopy

from pytest import fixture, raises

from api import create_app
from src.dependency_container import DependencyContainer


class TestApi:
    """Abstract class for testing Server endpoints"""

    __metaclass__ = ABCMeta

    @fixture(autouse=True)
    def set_up(self):

        DependencyContainer.reset_singletons()

        self._app = create_app()
        self._client = self._app.test_client

        self._do_set_up()

    def _do_set_up(self):
        pass

    def assert_response(self, response, expected_value, ignore_fields=[]):
        loaded_value = response.get_json(force=True)
        self.__assert_values(loaded_value, expected_value, ignore_fields)

    def __assert_values(self, real_object, expected_object, ignore_fields=[], sort_lists=True):
        if isinstance(expected_object, dict):
            for key,value in list(expected_object.items()):
                assert key in real_object
                self.__assert_values(real_object[key], value, ignore_fields)
                #remove value so we know is checked
                real_object.pop(key)

            for key,value in real_object.items():
                if not value or key in ignore_fields:
                    continue
                raise AssertionError( key + " was not expected in response")

        elif isinstance(expected_object, list):
            if not isinstance(real_object, list):
                raise AssertionError("Expected a List of values")
            if len(real_object) != len(expected_object):
                raise AssertionError("List are not of same size: \n" + str(real_object) + "\n" + str(expected_object))
            if(sort_lists):
                real_object.sort(key=self.__get_object_key_for_sorting)
                expected_object.sort(key=self.__get_object_key_for_sorting)
            for i in range(len(real_object)):
                self.__assert_values(real_object[i], expected_object[i], ignore_fields)
        else:
            assert real_object == expected_object

    def __get_object_key_for_sorting(self, object):
        if isinstance(object, dict):
            return "".join(object.keys())
        return object

    def test_check_value_simple_object(self):
        object = {
            "key" : "value"
        }
        self.__assert_values(real_object=object, expected_object=object)

    def test_check_value_simple_object_null_value(self):
        expected_object = {
            "key" : "value"
        }
        real_object = deepcopy(expected_object)
        real_object['key2'] = None
        self.__assert_values(real_object=real_object, expected_object=expected_object)
        with raises(AssertionError):
            self.__assert_values(expected_object, real_object)

    def test_check_value_list(self):
        object = [
            {
                "key" : "value"
            }
        ]
        self.__assert_values(real_object=object, expected_object=object)

    def test_check_value_list_not_sorted(self):
        real_object = [
            {
                "key1": "value1"
            },
            {
                "key2": "value2"
            }
        ]
        expected_object = [
            {
                "key2": "value2"
            },
            {
                "key1": "value1"
            }
        ]
        self.__assert_values(real_object=real_object, expected_object=expected_object)

    def test_assert_values_lists_different_size(self):
        real_object = [
            {
                "key1": "value1"
            }
        ]
        expected_object = deepcopy(real_object)
        expected_object.append({
            "key2" : "value2"
        })
        with raises(AssertionError):
            self.__assert_values(real_object=real_object, expected_object=expected_object)
        with raises(AssertionError):
            self.__assert_values(real_object=expected_object, expected_object=real_object)

    def test_assert_values_complex_object(self):
        real_object = {
            "key" : "value",
            "object_key" : {
                "second_object_key" : [
                    {
                        "object_in_list_key1" : "object_in_list_value1"
                    },
                    {
                        "object_in_list_key2": "object_in_list_value2",
                        "somethingElse" : None
                    },
                ]
            },
            "list_key": [
              1,2,3,4,5
            ]
        }
        expected_object = {
            "key" : "value",
            "list_key": [
                5,4,3,2,1
            ],
            "object_key": {
                "second_object_key": [
                    {
                        "object_in_list_key2": "object_in_list_value2"
                    },
                    {
                        "object_in_list_key1": "object_in_list_value1"
                    }
                ]
            },
        }
        self.__assert_values(real_object=real_object, expected_object=expected_object)
        with raises(AssertionError):
            self.__assert_values(real_object=real_object, expected_object=expected_object, sort_lists=False)


    def test_ignore_fields_simple_key(self):
        real_object = {
            "key1" : "value1",
            "key2" : "value2"
        }

        expected_object = {
            "key2" : "value2"
        }
        self.__assert_values(real_object=real_object, expected_object=expected_object, ignore_fields=['key1'])

    def test_ignore_fields_complex_key(self):
        real_object = {
            "keyA": {
                "keyB" : {
                    "keyC" : {
                        "key1" : "value1",
                        "key2" : "value2"
                    }
                }
            }
        }

        expected_object = {
            "keyA": {
                "keyB" : {
                    "keyC" : {
                        "key2" : "value2"
                    }
                }
            }
        }
        self.__assert_values(real_object=real_object, expected_object=expected_object, ignore_fields=['key1'])