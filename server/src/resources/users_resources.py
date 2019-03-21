'''
This file handles resources for creating, deleting, and updating information related to users.
'''
from marshmallow import Schema, fields, post_load

from src.core.user.user import User
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource


class UserListResource(AbstractResource):

    def __init__(self, **kwargs):
        super(UserListResource, self).__init__(**kwargs)
        self.__user_manager = DependencyContainer.user_manager()
        self.__users_schema = UserSchema(many=True)
        self.__user_schema = UserSchema()

    def _do_get(self):
        return self.__users_schema.dumps(self.__user_manager.get_all_users())

    def _do_post(self):
        user = self.__user_schema.loads(self._get_post_data_as_json()).data
        return self.__user_schema.dumps(self.__user_manager.add_user(user))


class UserResource(AbstractResource):

    def __init__(self, **kwargs):
        super(UserResource, self).__init__(**kwargs)
        self.__user_manager = DependencyContainer.user_manager()
        self.__user_schema = UserSchema()

    def _do_get(self, user_id):
        return self.__user_schema.dumps(self.__user_manager.get_user(user_id))


class UserSchema(Schema):

    id = fields.String(required=True)
    name = fields.String()
    position = fields.String(required=True)

    @post_load
    def make_user(self, kwargs):
        return User(**kwargs)