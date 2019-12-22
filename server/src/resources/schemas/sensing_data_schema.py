from marshmallow import Schema, fields, post_load

from src.core.data.sensing_data import SensingData


class SensingDataSchema(Schema):
    """
    Schema for serializing and deserializing sensed information corresponding to one sensor related to one object.
    """

    distance = fields.Number(required=True)
    timestamp = fields.Number(required=True)

    @post_load
    def make_sensed_data(self, kwargs):
        distance = kwargs.pop('distance')

        timestamp = kwargs.pop('timestamp')
        return SensingData(distance=distance, timestamp=timestamp)