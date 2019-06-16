from marshmallow import Schema, fields, post_load, post_dump


class PositionSchema(Schema):
    """
    Schema that represents a position in the system.
    """

    x = fields.Number(required=True)
    y = fields.Number(required=True)

    @post_load
    def make_position(self, kwargs):
        x = kwargs['x']
        y = kwargs['y']
        return (x, y)

    @post_dump(pass_original=True)
    def post_dump(self, serialized, original):
        serialized['x'] = original[0]
        serialized['y'] = original[1]