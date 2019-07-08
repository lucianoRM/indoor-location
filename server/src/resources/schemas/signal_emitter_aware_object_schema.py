from marshmallow import Schema, fields

from src.resources.schemas.dict_field import DictField
from src.resources.schemas.signal_emitter_schema import SignalEmitterSchema


class SignalEmitterAwareObjectSchema(Schema):
    signal_emitters = DictField(key_field=fields.String(), nested_field=fields.Nested(SignalEmitterSchema), missing={})
