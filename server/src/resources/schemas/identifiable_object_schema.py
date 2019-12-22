from abc import ABCMeta

from marshmallow import fields, ValidationError, validates_schema, Schema

class IdentifiableObjectSchema(Schema):
    """
    Base schema for a identifiable object in the system
    """

    __metaclass__ = ABCMeta

    __ID_KEY = 'id'

    id = fields.String(required=True)
    name = fields.String(missing=None)