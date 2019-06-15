from abc import ABCMeta, abstractmethod
from copy import deepcopy

from marshmallow import fields, post_dump, post_load, ValidationError, validates_schema, Schema

from src.resources.schemas.positionable_object_schema import PositionableObjectSchema


class TypedObjectSchema(PositionableObjectSchema):
    """
    Base schema for all objects that have a type attribut
    """

    __metaclass__ = ABCMeta

    __TYPE_ATTRIBUTE_KEY = 'type'

    type = fields.String()

    @validates_schema
    def validate_input(self, serialized_data):
        super().validate_input(serialized_data=serialized_data)

    @abstractmethod
    def _get_valid_types(self):
        return []

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

    def _get_type_schema(self, type):
        return None

    def __with_updated_fields(self, other_schema: Schema, func: callable, *args, **kwargs):
        original_declared_fields = self.declared_fields
        original_fields = self.fields
        if other_schema:
            all_declared_fields = deepcopy(original_declared_fields)
            all_fields = deepcopy(original_fields)
            all_declared_fields.update(other_schema.declared_fields)
            all_fields.update(other_schema.fields)
            self.declared_fields = all_declared_fields
            self.fields = all_fields
        result = func(*args, **kwargs)
        self.fields = original_fields
        self.declared_fields = original_declared_fields
        return result

    def load(self, data, **kwargs):
        if self.__TYPE_ATTRIBUTE_KEY not in data:
            raise ValidationError("Missing " + self.__TYPE_ATTRIBUTE_KEY)
        type = data[self.__TYPE_ATTRIBUTE_KEY]
        if type not in self._get_valid_types():
            raise ValidationError("Got wrong type: " + type + ", expecting one of: " + ", ".join(self._get_valid_types()))
        type_schema = self._get_type_schema(type)
        return self.__with_updated_fields(type_schema, super().load, data, False, **kwargs)


    def dump(self, object, **kwargs):
        type = self._get_object_type(object)
        type_schema = self._get_type_schema(type)
        return self.__with_updated_fields(type_schema, super().dump, object, **kwargs)




