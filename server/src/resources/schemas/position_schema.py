from marshmallow import Schema, fields, post_load, post_dump

from src.core.data.normalization_service import normalize_length


class PositionSchema(Schema):

    x = fields.Number(required=True)
    y = fields.Number(required=True)
    unit = fields.String()

    @post_load
    def make_position(self, kwargs):
        x = kwargs['x']
        y = kwargs['y']
        unit = kwargs.get('unit')
        normalized_x = normalize_length(x, unit)
        normalized_y = normalize_length(y, unit)
        return (normalized_x, normalized_y)

    @post_dump(pass_original=True)
    def post_dump(self, serialized, original):
        serialized['x'] = original[0]
        serialized['y'] = original[1]