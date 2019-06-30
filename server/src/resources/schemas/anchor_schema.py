from marshmallow import post_load

from src.core.anchor.anchor import Anchor
from src.resources.schemas.sensor_aware_object_schema import SensorAwareObjectSchema
from src.resources.schemas.signal_emitter_aware_object_schema import SignalEmitterAwareObjectSchema
from src.resources.schemas.static_object_schema import StaticObjectSchema


class AnchorSchema(StaticObjectSchema, SensorAwareObjectSchema, SignalEmitterAwareObjectSchema):

    @post_load
    def make_object(self, kwargs):
        return Anchor(**kwargs)
