from marshmallow import fields, Schema


class LogSchema(Schema):

    tag = fields.String(required=True, missing="NO_TAG")
    message = fields.String(required=True, missing="")
