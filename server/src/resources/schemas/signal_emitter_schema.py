from marshmallow import fields, post_load

from src.core.emitter.signal_emitter import SignalEmitter
from src.resources.schemas.identifiable_object_schema import IdentifiableObjectSchema


class SignalEmitterSchema(IdentifiableObjectSchema):
    signal = fields.Dict(missing={})

    @post_load
    def make_object(self, kwargs):
        return SignalEmitter(**kwargs)
