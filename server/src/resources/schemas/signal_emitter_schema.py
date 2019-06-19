from marshmallow import fields

from src.resources.schemas.identifiable_object_schema import IdentifiableObjectSchema


class SignalEmitterSchema(IdentifiableObjectSchema):

    signal = fields.Dict(required=True)