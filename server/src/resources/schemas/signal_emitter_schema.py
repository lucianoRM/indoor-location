from marshmallow import fields

from src.resources.schemas.identifiable_object_schema import IdentifiableObjectSchema

SIGNAL_EMITTER_TYPE = "SIGNAL_EMITTER"

class SignalEmitterSchema(IdentifiableObjectSchema):

    signal = fields.Dict(missing={})