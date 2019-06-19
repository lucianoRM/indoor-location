from abc import ABCMeta

from marshmallow import fields, ValidationError, validates_schema, Schem

class IdentifiableObjectSchema(Schema):
    """
    Base schema for a identifiable object in the system
    """

    __metaclass__ = ABCMeta

    __ID_KEY = 'id'

    id = fields.String()
    name = fields.String()

    @validates_schema
    def validate_input(self, serialized_data):
        super().validate_input(serialized_data)
        if self.__ID_KEY not in serialized_data:
            raise ValidationError(message="Missing " + self.__ID_KEY)