from marshmallow import Schema


class Serializer:

    def __init__(self, schema: Schema):
        self.__schema = schema

    def deserialize(self, data, **kwargs):
        return self.__schema.load(data=data, **kwargs).data

    def __dump_list(self, object_list, **kwargs):
        dumped_objects = []
        for obj in object_list:
            dumped_objects.append(self.__dump_object(obj, **kwargs))
        return dumped_objects

    def __dump_object(self, obj, **kwargs):
        return self.__schema.dump(obj=obj, **kwargs).data

    def serialize(self, value, **kwargs):
        if isinstance(value, list):
            return self.__dump_list(value, **kwargs)
        return self.__dump_object(value, **kwargs)
