from abc import ABCMeta, abstractmethod

from src.core.anchor.anchor import Anchor
from src.core.anchor.sensing_anchor import SensingAnchor
from src.core.location.location_service import NotEnoughPointsException
from src.core.user.sensing_user import SensingUser
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.anchor_schema import ANCHOR_TYPE
from src.resources.schemas.sensed_object_schema import SensedObjectSchema
from src.resources.schemas.sensing_anchor_schema import SensingAnchorSchema
from src.resources.schemas.sensing_user_schema import SensingUserSchema
from src.resources.schemas.typed_object_serializer import SerializationContext, TypedObjectSerializer
from src.resources.schemas.user_schema import USER_TYPE


class AbstractSensorResource(AbstractResource):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._sensor_manager = DependencyContainer.sensors_manager()
        self._serializer = TypedObjectSerializer(contexts=[
            SerializationContext(type=ANCHOR_TYPE, schema=SensingAnchorSchema(strict=True), klass=SensingAnchor),
            SerializationContext(type=USER_TYPE, schema=SensingUserSchema(strict=True),
                                 klass=SensingUser),
        ])


class SensorListResource(AbstractSensorResource):
    """
    Resource related to sensors in the system
    """
    __custom_error_mappings = {
        'SensorAlreadyExistsException': {
            'code': 409,
            'message': lambda e : str(e)
        }
    }

    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings, **kwargs)

    def _do_get(self):
        return self._serializer.dump(self._sensor_manager.get_all_sensors())

    def _do_post(self):
        sensor = self._serializer.load(self._get_post_data_as_json())
        return self._serializer.dump(self._sensor_manager.add_sensor(sensor_id=sensor.id, sensor=sensor))


class SensorResource(AbstractSensorResource):
    """
    Resource related to one particular sensor in the system
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__sensed_objects_processor = DependencyContainer.sensed_objects_processor()
        self.__sensed_objects_schema = SensedObjectSchema(strict=True, many=True)

    def _do_get(self, sensor_id):
        return self._serializer.dump(self._sensor_manager.get_sensor(sensor_id=sensor_id))

    def _do_put(self, sensor_id):
        objects = self.__sensed_objects_schema.load(self._get_post_data_as_json()).data
        try:
            self.__sensed_objects_processor.process_sensed_objects(sensor_id=sensor_id, sensed_objects=objects)
        except NotEnoughPointsException:
            pass





