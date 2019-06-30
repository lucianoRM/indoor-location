from abc import ABCMeta, abstractmethod

from src.core.location.location_service import NotEnoughPointsException
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.sensed_object_schema import SensedObjectSchema

from src.resources.schemas.sensor_schema import SensorSchema
from src.resources.schemas.serializer import Serializer


class AbstractSensorResource(AbstractResource):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._sensor_manager = DependencyContainer.sensors_manager()
        self._serializer = Serializer(SensorSchema(strict=True))


class SensorListResource(AbstractSensorResource):
    """
    Resource related to sensors in the system
    """
    __custom_error_mappings = {
        'SensorAlreadyExistsException': {
            'code': 409,
            'message': lambda e: str(e)
        }
    }

    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings, **kwargs)

    def _do_get(self):
        return self._serializer.serialize(self._sensor_manager.get_all_sensors())

    def _do_post(self):
        sensor = self._serializer.deserialize(self._get_post_data_as_json())
        return self._serializer.serialize(self._sensor_manager.add_sensor(sensor_id=sensor.id, sensor=sensor))


class SensorResource(AbstractSensorResource):
    """
    Resource related to one particular sensor in the system
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__sensed_objects_processor = DependencyContainer.sensed_objects_processor()
        self.__sensed_objects_schema = SensedObjectSchema(strict=True, many=True)

    def _do_get(self, sensor_id):
        return self._serializer.serialize(self._sensor_manager.get_sensor(sensor_id=sensor_id))

    def _do_put(self, sensor_id):
        objects = self.__sensed_objects_schema.load(self._get_post_data_as_json()).data
        try:
            self.__sensed_objects_processor.process_sensed_objects(sensor_id=sensor_id, sensed_objects=objects)
        except NotEnoughPointsException:
            pass
