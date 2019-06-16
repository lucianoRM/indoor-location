from marshmallow import fields

from src.core.anchor.signal_emitting_anchor import SignalEmittingAnchor
from src.core.user.signal_emitting_user import SignalEmittingUser
from src.core.user.user import User
from src.resources.schemas.typed_object_schema import TypedObjectSchema


class SignalEmitterSchema(TypedObjectSchema):

    __USER_TYPE = "USER"
    __ANCHOR_TYPE = "ANCHOR"

    signal = fields.Dict()

    def _get_valid_types(self):
        return [self.__USER_TYPE, self.__ANCHOR_TYPE]

    def _do_make_object(self, type, kwargs):
        if type == self.__USER_TYPE:
            return SignalEmittingUser(**kwargs)
        else:
            return SignalEmittingAnchor(**kwargs)

    def _get_object_type(self, original_object):
        if isinstance(original_object, User):
            return self.__USER_TYPE
        else:
            return self.__ANCHOR_TYPE
