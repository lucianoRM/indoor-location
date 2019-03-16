'''
This file handles resources for creating, deleting, and updating information related to users.
'''

from flask import request
from marshmallow import Schema, fields, post_load
from marshmallow.base import FieldABC
from marshmallow.fields import Field

from src.core.user.user import User, ID_KEY, POSITION_KEY, NAME_KEY
from src.dependency_container import USER_MANAGER
from src.resources.abstract_resource import AbstractResource


class UserListResource(AbstractResource):

    def __init__(self, **kwargs):
        super(UserListResource, self).__init__(**kwargs)
        self.__user_manager = kwargs[USER_MANAGER]
        self.__users_schema = UserSchema(many=True)
        self.__user_schema = UserSchema()

    def _do_get(self):
        return self.__users_schema.dumps(self.__user_manager.get_all_users())

    def _do_post(self):
        user = self.__user_schema.load(request.form.to_dict()).data
        return self.__user_schema.dumps(self.__user_manager.add_user(user))


class UserResource(AbstractResource):

    def __init__(self, **kwargs):
        super(UserResource, self).__init__(**kwargs)
        self.__user_manager = kwargs[USER_MANAGER]
        self.__user_schema = UserSchema()

    def _do_get(self, user_id):
        return self.__user_schema.dumps(self.__user_manager.get_user(user_id))

    def _do_put(self, user_id):
        user = self.__user_manager.get_user(user_id)
        # If user does not exist, request should fail
        args = request.form.to_dict()
        if (args.has_key(POSITION_KEY)):
            # TODO: Validate position first
            user.position = args[POSITION_KEY]
        if (args.has_key(NAME_KEY)):
            user.name = args[NAME_KEY]
        return self.__user_schema.dumps(self.__user_manager.update_user(user_id, user))


class UserSensedInformationResource(AbstractResource):
    def __init__(self, **kwargs):
        super(UserSensedInformationResource, self).__init__(**kwargs)
        self.__user_manager = kwargs[USER_MANAGER]

    def _do_put(self, user_id):
        user = self.__user_manager.get_user(user_id)
        # If user does not exist, request should fail
        args = request.form.to_dict()
        if (args.has_key(POSITION_KEY)):
            # TODO: Validate position first
            user.position = args[POSITION_KEY]
        if (args.has_key(NAME_KEY)):
            user.name = args[NAME_KEY]
        return self.__user_schema.dumps(self.__user_manager.update_user(user_id, user))


class UserSchema(Schema):

    id = fields.String(required=True, attribute=ID_KEY)
    name = fields.String(required=True, attribute=NAME_KEY)
    position = fields.String(attribute=POSITION_KEY)

    @post_load
    def make_user(self, kwargs):
        return User(**kwargs)