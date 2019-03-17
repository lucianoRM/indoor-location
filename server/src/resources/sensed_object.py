from marshmallow import fields, Schema, post_load

from src.core.data.sensed_object import SensedObject
from src.resources.sensed_object_data import SensedDataSchema


class SensedObjectSchema(Schema):
    """
    Schema for serializing and deserialising the information related to one object being sensed by one sensor
    """

    #The id of the sensed object
    object_id = fields.String(required=True)

    #The data that was sensed by that object
    sensed_data = fields.Nested(SensedDataSchema)

    @post_load
    def make_sensed_object(self, **kwargs):
        return SensedObject(object_id=kwargs.get('object_id'),
                            data=kwargs.get('sensed_data'))


