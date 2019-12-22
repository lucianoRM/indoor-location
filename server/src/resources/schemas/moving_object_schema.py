from abc import ABCMeta

from marshmallow import fields

from src.resources.schemas.identifiable_object_schema import IdentifiableObjectSchema
from src.resources.schemas.position_schema import PositionSchema


class MovingObjectSchema(IdentifiableObjectSchema):
    """
    Base schema for a moving object in the system
    """

    __metaclass__ = ABCMeta

    position = fields.Nested(PositionSchema, missing={'x':0, 'y':0})
    attributes = fields.Dict(missing={})

