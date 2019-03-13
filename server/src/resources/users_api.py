'''
This file handles resources for creating, deleting, and updating information related to users.
'''

from flask import request
from marshmallow import Schema, fields, post_load

from src.core.user.user import User, ID_KEY, LOCATION_KEY, NAME_KEY
from src.dependency_container import USER_MANAGER
from src.resources.abstract_resource import AbstractResource


class UserListAPI(AbstractResource):

    def __init__(self, **kwargs):
        super(UserListAPI, self).__init__(**kwargs)
        self.__user_manager = kwargs[USER_MANAGER]
        self.__users_schema = UserSchema(many=True)
        self.__user_schema = UserSchema()

    def _do_get(self):
        return self.__users_schema.dumps(self.__user_manager.get_all_users())

    def _do_post(self):
        user = self.__user_schema.load(request.form.to_dict()).data
        return self.__user_schema.dumps(self.__user_manager.add_user(user))


class UserAPI(AbstractResource):

    def __init__(self, **kwargs):
        super(UserAPI, self).__init__(**kwargs)
        self.__user_manager = kwargs[USER_MANAGER]
        self.__user_schema = UserSchema()

    def _do_get(self, user_id):
        return self.__user_schema.dumps(self.__user_manager.get_user(user_id))


class UserSchema(Schema):

    id = fields.String(required=True, attribute=ID_KEY)
    name = fields.String(required=True, attribute=NAME_KEY)
    location = fields.String(attribute=LOCATION_KEY)

    @post_load
    def make_user(self, args):
        return User(**args)