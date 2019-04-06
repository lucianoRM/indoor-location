from abc import ABCMeta

from marshmallow import Schema, fields


class PositionableObjectSchema(Schema):
    """
    Base schema for a positionable object in the system
    """

    __metaclass__ = ABCMeta

    id = fields.String(required=True)
    position = fields.String(required=True)

    name = fields.String()