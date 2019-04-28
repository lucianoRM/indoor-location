from abc import ABCMeta, abstractmethod

from marshmallow import Schema, fields, ValidationError, validates_schema, post_load

from src.resources.schemas.position_schema import PositionSchema


class PositionableObjectSchema(Schema):
    """
    Base schema for a positionable object in the system
    """

    __metaclass__ = ABCMeta

    __ID_KEY = 'id'
    __POSITION_KEY = 'position'

    id = fields.String()
    position = fields.Nested(PositionSchema)

    name = fields.String()

    @validates_schema
    def validate_input(self, serialized_data):
        if self.__ID_KEY not in serialized_data:
            raise ValidationError(message="Missing " + self.__ID_KEY)
        if self.__POSITION_KEY not in serialized_data:
            raise ValidationError("Missing " + self.__POSITION_KEY)

    @post_load
    def make_object(self, kwargs):
        return self._do_make_object(type=type, kwargs=kwargs)

    @abstractmethod
    def _do_make_object(self, type, kwargs):
        raise NotImplementedError