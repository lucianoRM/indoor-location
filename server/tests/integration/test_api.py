import json
from abc import ABCMeta
from copy import deepcopy
from unittest import TestCase

from api import create_app


class ApiTestCase(TestCase):
    """Abstract class for testing Server endpoints"""

    __metaclass__ = ABCMeta

    def setUp(self):
        self._app = create_app()
        self._client = self._app.test_client

    def assert_response(self, response, expected_value):
        loaded_value = json.loads(response.get_json())
        self.__assert_values(loaded_value, expected_value)

    def __assert_values(self, real_object, expected_object, sort_lists=True):
        if isinstance(expected_object, dict):
            for key,value in expected_object.items():
                self.assertTrue(real_object.has_key(key))
                self.__assert_values(real_object[key], value)
                #remove value so we know is checked
                real_object.pop(key)

            for key,value in real_object.items():
                if not value:
                    continue
                self.fail( key + " was not expected in response")

        elif isinstance(expected_object, list):
            if not isinstance(real_object, list):
                self.fail("Expected a List of values")
            if len(real_object) != len(expected_object):
                self.fail("List are not of same size: \n" + str(real_object) + "\n" + str(expected_object))
            if(sort_lists):
                real_object.sort()
                expected_object.sort()
            for i in range(len(real_object)):
                self.__assert_values(real_object[i], expected_object[i])
        else:
            self.assertEquals(real_object, expected_object)


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
        self.assertRaises(AssertionError, self.__assert_values, expected_object, real_object)

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
        self.assertRaises(AssertionError, self.__assert_values, real_object=real_object, expected_object=expected_object)
        self.assertRaises(AssertionError, self.__assert_values, real_object=expected_object, expected_object=real_object)

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
        self.assertRaises(AssertionError, self.__assert_values, real_object=real_object, expected_object=expected_object, sort_lists=False)