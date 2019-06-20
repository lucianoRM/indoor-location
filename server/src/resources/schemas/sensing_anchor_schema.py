from marshmallow import post_load

from src.core.anchor.sensing_anchor import SensingAnchor
from src.resources.schemas.anchor_schema import AnchorSchema
from src.resources.schemas.sensor_schema import SensorSchema

class SensingAnchorSchema(SensorSchema, AnchorSchema):

    @post_load
    def make_object(self, kwargs):
        return SensingAnchor(**kwargs)