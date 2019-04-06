
from src.core.sensor.sensor import Sensor
from src.core.user.sensing_user import SensingUser
from src.core.user.signal_emitting_user import SignalEmittingUser
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.typed_object_schema import TypedObjectSchema


class UserListResource(AbstractResource):
    '''
    Resource representing Users in the system
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__user_manager = DependencyContainer.users_manager()
        self.__users_schema = UserSchema(many=True, strict=True)
        self.__user_schema = UserSchema(strict=True)

    def _do_get(self):
        return self.__users_schema.dumps(self.__user_manager.get_all_users())

    def _do_post(self):
        user = self.__user_schema.loads(self._get_post_data_as_json()).data
        return self.__user_schema.dumps(self.__user_manager.add_user(user_id=user.id, user=user))


class UserResource(AbstractResource):
    '''
    Resource related to one user in particular in the system
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__user_manager = DependencyContainer.users_manager()
        self.__user_schema = UserSchema(strict=True)

    def _do_get(self, user_id):
        return self.__user_schema.dumps(self.__user_manager.get_user(user_id=user_id))


class UserSchema(TypedObjectSchema):

    __SENSOR_TYPE = "SENSOR"
    __SIGNAL_EMITTER_TYPE = "SIGNAL_EMITTER"

    def _get_valid_types(self):
        return [self.__SENSOR_TYPE, self.__SIGNAL_EMITTER_TYPE]

    def _do_make_object(self, type, kwargs):
        if type == self.__SENSOR_TYPE:
            return SensingUser(**kwargs)
        else:
            return SignalEmittingUser(**kwargs)

    def _get_object_type(self, original_object):
        if isinstance(original_object, Sensor):
            return self.__SENSOR_TYPE
        else:
            return self.__SIGNAL_EMITTER_TYPE



