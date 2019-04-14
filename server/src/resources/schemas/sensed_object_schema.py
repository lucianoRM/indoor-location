from marshmallow import fields, Schema, post_load

from src.core.data.sensed_object import SensedObject
from src.resources.schemas.dict_field import DictField
from src.resources.schemas.sensing_data_schema import SensingDataSchema


class SensedObjectSchema(Schema):
    """
    Schema for serializing and deserialising the information related to one object being sensed by one sensor
    """

    #The id of the sensed object
    id = fields.String(required=True)

    #The data that was sensed by that object
    sensed_data = fields.Nested(SensingDataSchema, required=True)

    @post_load
    def make_sensed_object(self, kwargs):
        return SensedObject(id=kwargs.pop('id'),
                            data=kwargs.pop('sensed_data'),
                            sensor=None)



class SensedObjectsSchema(Schema):

    sensed_objects = DictField(
        key_field=fields.String(),
        nested_field=fields.Nested(SensedObjectSchema)
    )

    @post_load
    def make_dict(self, kwargs):
        return kwargs['sensed_objects']


