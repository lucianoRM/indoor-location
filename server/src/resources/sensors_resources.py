'''
This file handles resources for creating, deleting, and updating information related to sensors.
'''

from flask import request
from marshmallow import Schema, fields, post_load

from src.core.sensor.sensor import Sensor, ID_KEY, LOCATION_KEY, NAME_KEY
from src.dependency_container import SENSOR_MANAGER
from src.resources.abstract_resource import AbstractResource


class SensorListResource(AbstractResource):

    def __init__(self, **kwargs):
        super(SensorListResource, self).__init__(**kwargs)
        self.__sensor_manager = kwargs[SENSOR_MANAGER]
        self.__sensors_schema = SensorSchema(many=True)
        self.__sensor_schema = SensorSchema()

    def _do_get(self):
        return self.__sensors_schema.dumps(self.__sensor_manager.get_all_sensors())

    def _do_post(self):
        sensor = self.__sensor_schema.load(request.form.to_dict()).data
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
        args = request.form.to_dict()
        if (args.has_key(LOCATION_KEY)):
            # TODO: Validate location first
            sensor.location = args[LOCATION_KEY]
        if (args.has_key(NAME_KEY)):
            sensor.name = args[NAME_KEY]
        return self.__sensor_schema.dumps(self.__sensor_manager.update_sensor(sensor_id, sensor))


class SensorSchema(Schema):

    id = fields.String(required=True, attribute=ID_KEY)
    name = fields.String(required=True, attribute=NAME_KEY)
    location = fields.String(attribute=LOCATION_KEY)

    @post_load
    def make_sensor(self, kwargs):
        return Sensor(**kwargs)