from marshmallow import Schema, fields, post_load
from measurement.measures import Distance

from src.core.data.sensing_data import SensingData


class SensedObjectInformationSchema(Schema):
    """
    Schema for serializing and deserializing sensed information corresponding to one sensor related to one object.
    """

    distance = fields.Number(required=True)
    distance_unit = fields.String(required=True)
    timestamp = fields.Number(required=True)

    @post_load
    def make_sensed_data(self, kwargs):
        distance_value = kwargs.pop('distance')
        distance_unit = kwargs.pop('distance_unit')
        distance = Distance(**{distance_unit:distance_value})

        timestamp = kwargs.pop('timestamp')
        return SensingData(distance=distance,timestamp=timestamp)