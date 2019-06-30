from marshmallow import post_load

from src.core.sensor.sensor import Sensor
from src.resources.schemas.identifiable_object_schema import IdentifiableObjectSchema


class SensorSchema(IdentifiableObjectSchema):

    @post_load
    def make_object(self, kwargs):
        return Sensor(**kwargs)
