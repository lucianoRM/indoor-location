import flask_restful
from flask_restful import Resource, HTTPException
from werkzeug.exceptions import NotFound


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
        if(self.__common_error_mappings.has_key(error_class_name)):
            error = self.__common_error_mappings.get(error_class_name)
        if self.__custom_error_mappings.has_key(error_class_name):
            error = self.__custom_error_mappings.get(error_class_name)
        code = error.get('code', 500)
        message = error.get('message', e.message)
        flask_restful.abort(code, message=message)

    def get(self, **kwargs):
        """
        Base method for implementing HTTP GET requests.
        Child classes should not re implement this, but the Template method: _do_get
        :param args: args defined in the url
        :param kwargs: extra kwargs
        :return: the response to send to the client
        """
        return self.__execute_handling(self._do_get, **kwargs)

    def post(self, **kwargs):
        """
        Base method for implementing HTTP POST requests.
        Child classes should not re implement this, but the Template method: _do_post
        :param args: args defined in the url
        :param kwargs: extra kwargs
        :return: the response to send to the client
        """
        return self.__execute_handling(self._do_post, **kwargs)

    def _do_get(self, **kwargs):
        """
        Template method to implement for handling an HTTP GET on the resource
        :param args: uri parameters
        :param kwargs: extra kwargs
        :return: processed response
        """
        raise NotFound()

    def _do_post(self, **kwargs):
        """
        Template method to implement for handling an HTTP POST on the resource
        :param args: uri parameters
        :param kwargs: extra kwargs
        :return: processed response
        """
        raise NotFound()