from abc import ABCMeta

from marshmallow import fields, ValidationError, validates_schema

from src.resources.schemas.identifiable_object_schema import IdentifiableObjectSchema
from src.resources.schemas.position_schema import PositionSchema


class StaticObjectSchema(IdentifiableObjectSchema):
    """
    Base schema for a static object in the system
    """

    __metaclass__ = ABCMeta

    __POSITION_KEY = 'position'

    position = fields.Nested(PositionSchema)

    @validates_schema
    def validate_input(self, serialized_data):
        super().validate_input(serialized_data)
        if self.__POSITION_KEY not in serialized_data:
            raise ValidationError("Missing " + self.__POSITION_KEY)