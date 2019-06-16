from src.core.sensor.sensor import Sensor
from src.core.user.sensing_user import SensingUser
from src.core.user.signal_emitting_user import SignalEmittingUser
from src.core.user.user import User
from src.resources.schemas.signal_emitter_schema import SignalEmitterSchema
from src.resources.schemas.typed_object_schema import TypedObjectSchema


class UserSchema(TypedObjectSchema):

    __SENSOR_TYPE = "SENSOR"
    __SIGNAL_EMITTER_TYPE = "SIGNAL_EMITTER"

    __SIGNAL_EMITTER_SCHEMA = SignalEmitterSchema()

    def _get_valid_types(self):
        return [self.__SENSOR_TYPE, self.__SIGNAL_EMITTER_TYPE]

    def _get_type_schema(self, type):
        if type == self.__SIGNAL_EMITTER_TYPE:
            return self.__SIGNAL_EMITTER_SCHEMA
        return super()._get_type_schema(type)

    def _do_make_object(self, type, kwargs) -> User:
        if type == self.__SENSOR_TYPE:
            return SensingUser(**kwargs)
        else:
            return SignalEmittingUser(**kwargs)

    def _get_object_type(self, original_object):
        if isinstance(original_object, Sensor):
            return self.__SENSOR_TYPE
        else:
            return self.__SIGNAL_EMITTER_TYPE
