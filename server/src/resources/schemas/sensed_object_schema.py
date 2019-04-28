from marshmallow import fields, Schema, post_load

from src.core.data.sensed_object import SensedObject
from src.resources.schemas.sensing_data_schema import SensingDataSchema

class SensedObjectSchema(Schema):

    id = fields.String(required=True)
    data = fields.Nested(SensingDataSchema, required=True)

    @post_load
    def make_object(self, kwargs):
        id = kwargs["id"]
        data = kwargs["data"]
        return SensedObject(id=id, data=data)



