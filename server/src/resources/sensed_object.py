from marshmallow import fields, Schema
from measurement.measures import Distance


class SensedObjectSchema(Schema):

    id = fields.String(required=True)
    distance = fields.Number(required=True)
    distance_units = fields.String(required=True)

