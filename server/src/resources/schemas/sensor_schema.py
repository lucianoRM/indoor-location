from marshmallow import post_load

from src.core.sensor.sensor import Sensor
from src.resources.schemas.identifiable_object_schema import IdentifiableObjectSchema
from src.resources.schemas.moving_object_schema import MovingObjectSchema


class SensorSchema(MovingObjectSchema):

    @post_load
    def make_object(self, kwargs):
        return Sensor(**kwargs)
