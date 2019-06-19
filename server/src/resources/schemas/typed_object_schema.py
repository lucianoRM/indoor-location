from abc import abstractmethod
from copy import deepcopy
from typing import List

from marshmallow import fields, post_dump, post_load, ValidationError, Schema


class SerializationContext:

    def __init__(self, type, schema, klass, implementation):
        self.__type = type
        self.__schema = schema
        self.__implementation = implementation
        self.__klass = klass

    @property
    def type(self):
        return self.__type

    @property
    def schema(self):
        return self.__schema

    @property
    def constructor(self):
        return self.__implementation

    @property
    def klass(self):
        return self.__klass

class TypedObjectSchema(Schema):
    """
    Base schema for all objects that have a type attribut
    """

    __TYPE_ATTRIBUTE_KEY = 'type'

    type = fields.String()

    def __init__(self, main_schema: Schema, contexts: List[SerializationContext], **kwargs):
        super().__init__(**kwargs)
        self.__main_schema = main_schema

        self.__contexts_by_type = {}
        self.__contexts_by_klass = {}
        for context in contexts:
            self.__contexts_by_type[context.type] = context
            self.__contexts_by_klass[context.klass] = context



    @abstractmethod
    def _get_valid_types(self):
        return []

    @post_load
    def make_object(self, kwargs):
        type = kwargs.pop(self.__TYPE_ATTRIBUTE_KEY)
        context = self.__contexts_by_type[type]
        return context.constructor(**kwargs)

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
        context = self.__contexts_by_klass[type(original_object)]
        serialized_object[self.__TYPE_ATTRIBUTE_KEY] = context.type

    def __with_updated_fields(self, other_schema: Schema, func: callable, *args, **kwargs):
        original_declared_fields = self.declared_fields
        original_fields = self.fields

        all_declared_fields = deepcopy(original_declared_fields)
        all_fields = deepcopy(original_fields)
        all_declared_fields.update(self.__main_schema.declared_fields)
        all_fields.update(self.__main_schema.fields)

        for declared_field_name, declared_field in other_schema.declared_fields.items():
            if declared_field_name in all_declared_fields:
                if all_declared_fields[declared_field_name].required:
                    continue
            all_declared_fields[declared_field_name] = declared_field

        for field_name, field in other_schema.fields.items():
            if field_name in all_fields:
                if all_fields[field_name].required:
                    continue
            all_fields[field_name] = field

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
        if type not in self.__contexts_by_type:
            raise ValidationError("Got wrong type: " + type + ", expecting one of: " + ", ".join(self._get_valid_types()))
        context = self.__contexts_by_type[type]
        return self.__with_updated_fields(context.schema, super().load, data, False, **kwargs)


    def dump(self, value, **kwargs):
        value_context = None
        for klass, context in self.__contexts_by_klass.items():
            if isinstance(value, klass):
                value_context = context
                break
        if not value_context:
            raise ValidationError("Serializer is not configured to deserialize: " + str(type(value)))
        type_schema = value_context.schema
        return self.__with_updated_fields(type_schema, super().dump, value, **kwargs)




