from marshmallow import Schema, fields, post_load

from src.core.data.normalization_service import normalize_length


class DistanceSchema(Schema):

    value = fields.Number(required=True)
    unit = fields.String()

    @post_load
    def make_distance(self, kwargs):
        distance = kwargs['value']
        distance_unit = kwargs['unit']
        return normalize_length(distance, distance_unit)