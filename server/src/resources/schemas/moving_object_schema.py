from abc import ABCMeta

from marshmallow import fields

from src.resources.schemas.identifiable_object_schema import IdentifiableObjectSchema
from src.resources.schemas.position_schema import PositionSchema


class MovingObjectSchema(IdentifiableObjectSchema):
    """
    Base schema for a moving object in the system
    """

    __metaclass__ = ABCMeta

    __POSITION_KEY = 'position'

    position = fields.Nested(PositionSchema)

    def validate_input(self, serialized_data):
        super().validate_input(serialized_data)

