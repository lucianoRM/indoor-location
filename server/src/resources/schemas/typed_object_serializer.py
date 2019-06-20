from abc import abstractmethod
from copy import deepcopy
from typing import List

from marshmallow import fields, post_dump, post_load, ValidationError, Schema


class SerializationContext:

    def __init__(self, type, schema, klass):
        self.__type = type
        self.__schema = schema
        self.__klass = klass

    @property
    def type(self):
        return self.__type

    @property
    def schema(self):
        return self.__schema

    @property
    def klass(self):
        return self.__klass

class TypedObjectSerializer:
    """
    Base serializer for all objects that have a type attribute
    """
    __TYPE_ATTRIBUTE_KEY = 'type'

    def __init__(self, contexts: List[SerializationContext]):
        self.__contexts_by_type = {}
        self.__contexts_by_klass = {}
        for context in contexts:
            self.__contexts_by_klass[context.klass] = context
            self.__contexts_by_type[context.type] = context

    def load(self, data, **kwargs):
        if self.__TYPE_ATTRIBUTE_KEY not in data:
            raise ValidationError("Missing " + self.__TYPE_ATTRIBUTE_KEY)
        type = data[self.__TYPE_ATTRIBUTE_KEY]
        if type not in self.__contexts_by_type:
            raise ValidationError("Got wrong type: " + type + ", expecting one of: " + ", ".join(self.__contexts_by_type.keys()))
        context = self.__contexts_by_type[type]
        return context.schema.load(data=data, **kwargs)

    def __dump_list(self, object_list, **kwargs):
        dumped_objects = []
        for obj in object_list:
            dumped_objects.append(self.__dump_object(obj, **kwargs))
        return dumped_objects

    def __dump_object(self, obj, **kwargs):
        context = self.__contexts_by_klass.get(type(obj), None)
        if not context:
            raise ValidationError("Serializer is not configured to deserialize a: " + str(type(obj)))
        dumped = context.schema.dump(obj=obj, **kwargs).data
        dumped[self.__TYPE_ATTRIBUTE_KEY] = context.type
        return dumped

    def dump(self, value, **kwargs):
        if isinstance(value, list):
            return self.__dump_list(value, **kwargs)
        return self.__dump_object(value, **kwargs)




