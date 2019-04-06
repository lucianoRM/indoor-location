
from src.core.anchor.sensing_anchor import SensingAnchor
from src.core.user.sensing_user import SensingUser
from src.core.user.user import User
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.sensed_object import SensedObjectSchema
from src.resources.schemas.typed_object_schema import TypedObjectSchema


class SensorListResource(AbstractResource):
    """
    Resource related to sensors in the system
    """

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
    """
    Resource related to one particular sensor in the system
    """

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


class SensorSchema(TypedObjectSchema):

    __USER_TYPE = "USER"
    __ANCHOR_TYPE = "ANCHOR"

    def _do_make_object(self, type, kwargs):
        if type == self.__USER_TYPE:
            return SensingUser(**kwargs)
        else:
            return SensingAnchor(**kwargs)

    def _get_object_type(self, original_object):
        if isinstance(original_object, User):
            return self.__USER_TYPE
        else:
            return self.__ANCHOR_TYPE





