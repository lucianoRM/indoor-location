from abc import ABCMeta, abstractmethod
from typing import Callable

import flask_restful
from flask import request
from flask_restful import Resource
from werkzeug.exceptions import NotFound

APPLICATION_JSON = "application/json"

class AbstractResource(Resource):
    """
    Abstract class extending flask-restful Resource that adds extra common logic.
    """
    __metaclass__ = ABCMeta

    def __collect_validation_error_keys(self, context, actual):
        all_keys = []
        errors = []
        if "_schema" not in actual:
            if isinstance(actual, list):
                errors = actual
            elif isinstance(actual, dict):
                for key in actual:
                    context[key] = {}
                    next_level_keys = self.__collect_validation_error_keys(context[key], actual[key])
                    if not next_level_keys:
                        all_keys.append(key)
                    else:
                        for next_key in next_level_keys:
                            joiner = "."
                            if len(next_level_keys) == 0:
                                joiner = ""
                            elif len(next_level_keys) == 1:
                                joiner = ":"
                            all_keys.append(joiner.join([str(key), next_key]))
            else:
                errors = [str(actual)]
        else:
            errors = actual['_schema']
        for error in errors:
            all_keys.append(error)
        return all_keys

    def __get_validation_error_keys(self, messages):
        error_keys = []
        if isinstance(messages, list):
            error_keys = messages
        if isinstance(messages, dict):
            all_errors = {}
            error_keys = self.__collect_validation_error_keys(all_errors, messages)
        return error_keys

    @abstractmethod
    def __init__(self, custom_error_mappings=None, **kwargs):
        self.__default_error = {
            'code': 500
        }
        self.__common_error_mappings = {
            'NotFound': {
                'code': 404,
                'message': lambda e: 'Not Found'
            },
            'ValidationError': {
                'code': 400,
                'message': lambda e: "Invalid format: [" + ",".join(self.__get_validation_error_keys(e.messages)) + "]"
            }
        }

        self.__custom_error_mappings = custom_error_mappings if custom_error_mappings is not None else {}
        super().__init__(**kwargs)

    def __execute_handling(self, method: Callable, **kwargs):
        try:
            if not kwargs:
                return method()
            else:
                return method(**kwargs)
        except Exception as e:
            self.__handle_exception(e)

    def __handle_exception(self, e):
        error_class_name = e.__class__.__name__
        error = self.__default_error
        if error_class_name in self.__common_error_mappings:
            error = self.__common_error_mappings.get(error_class_name)
        if error_class_name in self.__custom_error_mappings:
            error = self.__custom_error_mappings.get(error_class_name)
        code = error.get('code', 500)
        message_getter = error.get('message', lambda e: str(e))
        message = message_getter(e)
        flask_restful.abort(code, errors=message)

    def _get_post_data_as_json(self):
        """
        Return post data as json or fail if not correctly formatter
        :return: the post value data correctly formatted as JSON
        """
        return request.get_json()

    def get(self, **kwargs):
        """
        Base method for implementing HTTP GET requests.
        Child classes should not re implement this, but the Template method: _Fdo_get
        :param kwargs: extra kwargs
        :return: the response to send to the client
        """
        return self.__execute_handling(self._do_get, **kwargs)

    def post(self, **kwargs):
        """
        Base method for implementing HTTP POST requests.
        Child classes should not re implement this, but the Template method: _do_post
        :param kwargs: extra kwargs
        :return: the response to send to the client
        """
        return self.__execute_handling(self._do_post, **kwargs)

    def put(self, **kwargs):
        """
        Base method for implementing HTTP PUT requests
        Child classes should not re implement this, but the Template method: _do_put
        :param kwargs: extra kwargs
        :return: the response to send to the client
        """
        return self.__execute_handling(self._do_put, **kwargs)

    def _do_get(self, **kwargs):
        """
        Template method to implement for handling an HTTP GET on the resource
        :param kwargs: extra kwargs
        :return: processed response
        """
        raise NotFound()

    def _do_post(self, **kwargs):
        """
        Template method to implement for handling an HTTP POST on the resource
        :param kwargs: extra kwargs
        :return: processed response
        """
        raise NotFound()

    def _do_put(self, **kwargs):
        """
        Template method to implement for handling an HTTP PUT on the resource
        :param kwargs: extra kwargs
        :return: pocessed response
        """
        raise NotFound()