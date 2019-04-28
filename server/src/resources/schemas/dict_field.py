from marshmallow.fields import Field


class DictField(Field):

    def __init__(self, key_field, nested_field, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.__key_field = key_field
        self.__nested_field = nested_field

    def _deserialize(self, value, *args, **kwargs):
        ret = {}
        for key, val in value.items():
            k = self.__key_field.deserialize(key)
            v = self.__nested_field.deserialize(val)
            ret[k] = v
        return ret

    def _serialize(self, value, attr, obj):
        ret = {}
        for key, val in value.items():
            k = self.__key_field._serialize(key, attr, obj)
            v = self.__nested_field.serialize(key, self.get_value(attr, obj))
            ret[k] = v
        return ret