from marshmallow import post_load

from src.core.user.sensing_user import SensingUser
from src.resources.schemas.sensor_schema import SensorSchema
from src.resources.schemas.user_schema import UserSchema

class SensingUserSchema(SensorSchema, UserSchema):

    @post_load
    def make_object(self, kwargs):
        return SensingUser(**kwargs)