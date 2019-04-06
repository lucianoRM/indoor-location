from abc import ABCMeta, abstractmethod

from marshmallow import Schema, fields, post_dump, post_load

from src.resources.schemas.positionable_object_schema import PositionableObjectSchema


class TypedObjectSchema(PositionableObjectSchema):
    """
    Base schema for all objects that have a type attribut
    """

    __metaclass__ = ABCMeta

    __TYPE_ATTRIBUTE_KEY = 'type'

    type = fields.String(required=True)

    @post_load
    def make_object(self, kwargs):
        type = kwargs.pop(self.__TYPE_ATTRIBUTE_KEY)
        return self._do_make_object(type=type, kwargs=kwargs)

    @abstractmethod
    def _do_make_object(self, type, kwargs):
        raise NotImplementedError

    @post_dump(pass_many=True, pass_original=True)
    def add_synthetic_data(self, serialized, many, original):
        serialized_values = serialized
        original_values = original
        if not many:
            serialized_values = [serialized]
            original_values = [original]

        for i in range(len(serialized_values)):
            self._add_synthetic_data(serialized_values[i], original_values[i])

    def _add_synthetic_data(self, serialized_object, original_object):
        serialized_object[self.__TYPE_ATTRIBUTE_KEY] = self._get_object_type(original_object)

    @abstractmethod
    def _get_object_type(self, original_object):
        raise NotImplementedError
