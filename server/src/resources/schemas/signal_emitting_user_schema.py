from marshmallow import post_load

from src.core.user.signal_emitting_user import SignalEmittingUser
from src.resources.schemas.signal_emitter_schema import SignalEmitterSchema
from src.resources.schemas.user_schema import UserSchema

class SignalEmittingUserSchema(SignalEmitterSchema, UserSchema):

    @post_load
    def make_object(self, kwargs):
        return SignalEmittingUser(**kwargs)