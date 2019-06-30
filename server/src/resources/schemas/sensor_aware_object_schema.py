from marshmallow import Schema, fields

from src.resources.schemas.sensor_schema import SensorSchema


class SensorAwareObjectSchema(Schema):
    sensors = fields.Dict(fields.Nested(SensorSchema), missing={})
