'''
This file handles resources for creating, deleting, and updating information related to sensors.
'''

from marshmallow import Schema, fields, post_load, post_dump

from src.core.anchor.anchor import Anchor
from src.core.anchor.sensing_anchor import SensingAnchor
from src.core.sensor.sensor import Sensor
from src.core.user.sensing_user import SensingUser
from src.core.user.user import User
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.sensed_object import SensedObjectSchema


class SensorListResource(AbstractResource):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__sensor_manager = DependencyContainer.sensors_manager()
        self.__sensors_schema = SensorSchema(many=True)
        self.__sensor_schema = SensorSchema()
        self.__sensed_objects_schema = SensedObjectSchema(many=True)

    def _do_get(self):
        return self.__sensors_schema.dumps(self.__sensor_manager.get_all_sensors())

    def _do_post(self):
        sensor = self.__sensor_schema.loads(self._get_post_data_as_json()).data
        return self.__sensor_schema.dumps(self.__sensor_manager.add_sensor(sensor_id=sensor.id, sensor=sensor))


class SensorResource(AbstractResource):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__sensor_manager = DependencyContainer.sensors_manager()
        self.__sensor_schema = SensorSchema()

    def _do_get(self, sensor_id):
        return self.__sensor_schema.dumps(self.__sensor_manager.get_sensor(sensor_id=sensor_id))

    def _do_put(self, sensor_id):
        sensor = self.__sensor_manager.get_sensor(sensor_id=sensor_id)
        # If sensor does not exist, request should fail
        sensed_objects = self.__sensed_objects_schema.loads(self._get_post_data_as_json()).data
        sensor.update_sensed_objects(sensed_objects=sensed_objects)
        return self.__sensor_schema.dumps(self.__sensor_manager.update_sensor(sensor_id=sensor_id, sensor=sensor))


class SensorSchema(Schema):

    USER = "USER"
    ANCHOR = "ANCHOR"
    TYPE_ARGUMENT = "type"

    id = fields.String(required=True)
    position = fields.String(required=True)
    type = fields.String(required=True)

    name = fields.String()

    @post_load
    def make_sensor(self, kwargs):
        type = kwargs.pop(self.TYPE_ARGUMENT)
        if type == self.USER:
            return SensingUser(**kwargs)
        else:
            return SensingAnchor(**kwargs)

    @post_dump(pass_many=True, pass_original=True)
    def add_synthetic_data(self, serialized, many, original):
        serialized_values = serialized
        original_values = original
        if not many:
            serialized_values = [serialized]
            original_values = [original]

        for i in range(len(serialized_values)):
            self.__add_synthetic_data(serialized_values[i], original_values[i])


    def __add_synthetic_data(self, serialized_value, original):
        if isinstance(original, User):
            serialized_value[self.TYPE_ARGUMENT] = self.USER
        elif isinstance(original, Anchor):
            serialized_value[self.TYPE_ARGUMENT] = self.ANCHOR




