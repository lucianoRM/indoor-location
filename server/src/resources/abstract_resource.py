import flask_restful
from flask import request
from flask_restful import Resource
from werkzeug.exceptions import NotFound

APPLICATION_JSON = "application/json"

class AbstractResource(Resource):
    """
    Abstract class extending flask-restful Resource that adds extra common logic.
    """

    def __init__(self, custom_error_mappings=None, **kwargs):
        self.__default_error = {
            'code': 500
        }
        self.__common_error_mappings = {
            'NotFound' : {
                'code' : 404,
                'message' : 'Not Found'
            }
        }

        self.__custom_error_mappings = custom_error_mappings if custom_error_mappings is not None else {}
        super().__init__(**kwargs)

    def __execute_handling(self, method, **kwargs):
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
        message = error.get('message', str(e))
        flask_restful.abort(code, message=message)

    def _get_post_data_as_json(self):
        """
        Return post data as json or fail if not correctly formatter
        :return: the post value data correctly formatted as JSON
        """
        return request.get_json(force=True)


    def get(self, **kwargs):
        """
        Base method for implementing HTTP GET requests.
        Child classes should not re implement this, but the Template method: _do_get
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