from marshmallow import Schema, fields, pre_dump, post_dump

from src.resources.schemas.dict_field import DictField
from src.resources.schemas.sensor_schema import SensorSchema


class SensorAwareObjectSchema(Schema):
    sensors = DictField(key_field=fields.String(), nested_field=fields.Nested(SensorSchema), missing={})

    @pre_dump()
    def pd(self,a):
        return a
