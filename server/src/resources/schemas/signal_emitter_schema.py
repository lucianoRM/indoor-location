from marshmallow import fields, post_load, post_dump

from src.core.emitter.signal_emitter import SignalEmitter
from src.resources.schemas.moving_object_schema import MovingObjectSchema


class SignalEmitterSchema(MovingObjectSchema):

    signal = fields.Dict(missing={})

    def __values_to_string(self, dict):
        for k in dict:
            dict[k] = str(dict[k])

    @post_load
    def make_object(self, kwargs):
        self.__values_to_string(kwargs['signal'])
        return SignalEmitter(**kwargs)

    @post_dump
    def fix_serialized(self, serialized):
        self.__values_to_string(serialized['signal'])
        return serialized

