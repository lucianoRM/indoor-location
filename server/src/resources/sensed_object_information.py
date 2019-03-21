from marshmallow import Schema, fields, post_load
from measurement.measures import Distance

from src.core.data.sensed_object_information import SensedObjectInformation


class SensedObjectInformationSchema(Schema):
    """
    Schema for serializing and deserializing sensed information corresponding to one sensor related to one object.
    """

    distance = fields.Number(required=True)
    distance_unit = fields.String(required=True)

    @post_load
    def make_sensed_data(self, kwargs):
        distance_value = kwargs.get('distance')
        distance_unit = kwargs.get('distance_unit')
        distance = Distance(**{distance_unit:distance_value})
        return SensedObjectInformation(distance=distance)