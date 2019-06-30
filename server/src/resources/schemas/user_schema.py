from marshmallow import post_load

from src.core.user.user import User
from src.resources.schemas.moving_object_schema import MovingObjectSchema
from src.resources.schemas.sensor_aware_object_schema import SensorAwareObjectSchema
from src.resources.schemas.signal_emitter_aware_object_schema import SignalEmitterAwareObjectSchema


class UserSchema(MovingObjectSchema, SensorAwareObjectSchema, SignalEmitterAwareObjectSchema):

    @post_load
    def make_object(self, kwargs):
        return User(**kwargs)
