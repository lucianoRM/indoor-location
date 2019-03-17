'''
This file handles resources for creating, deleting, and updating information related to sensors.
'''

from flask import request
from marshmallow import Schema, fields, post_load

from src.core.sensor.sensor import Sensor
from src.dependency_container import SENSOR_MANAGER
from src.resources.abstract_resource import AbstractResource
from src.resources.sensed_object import SensedObjectSchema


class SensorListResource(AbstractResource):

    def __init__(self, **kwargs):
        super(SensorListResource, self).__init__(**kwargs)
        self.__sensor_manager = kwargs[SENSOR_MANAGER]
        self.__sensors_schema = SensorSchema(many=True)
        self.__sensor_schema = SensorSchema()
        self.__sensed_objects_schema = SensedObjectSchema(many=True)

    def _do_get(self):
        return self.__sensors_schema.dumps(self.__sensor_manager.get_all_sensors())

    def _do_post(self):
        sensor = self.__sensor_schema.loads(self._get_post_data_as_json()).data
        return self.__sensor_schema.dumps(self.__sensor_manager.add_sensor(sensor))


class SensorResource(AbstractResource):

    def __init__(self, **kwargs):
        super(SensorResource, self).__init__(**kwargs)
        self.__sensor_manager = kwargs[SENSOR_MANAGER]
        self.__sensor_schema = SensorSchema()

    def _do_get(self, sensor_id):
        return self.__sensor_schema.dumps(self.__sensor_manager.get_sensor(sensor_id))

    def _do_put(self, sensor_id):
        sensor = self.__sensor_manager.get_sensor(sensor_id)
        # If sensor does not exist, request should fail
        sensed_objects = self.__sensed_objects_schema.loads(self._get_post_data_as_json()).data
        sensor.update_sensed_objects(sensed_objects=sensed_objects)
        return self.__sensor_schema.dumps(self.__sensor_manager.update_sensor(sensor_id, sensor))


class SensorSchema(Schema):

    id = fields.String(required=True)
    name = fields.String()
    position = fields.String(required=True)

    @post_load
    def make_sensor(self, kwargs):
        return Sensor(**kwargs)




