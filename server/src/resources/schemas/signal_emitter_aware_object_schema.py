from marshmallow import Schema, fields

from src.resources.schemas.signal_emitter_schema import SignalEmitterSchema


class SignalEmitterAwareObjectSchema(Schema):
    signal_emitters = fields.Dict(fields.Nested(SignalEmitterSchema), missing={})
