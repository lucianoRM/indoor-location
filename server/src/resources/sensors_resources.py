from abc import ABCMeta, abstractmethod

from src.core.data.sensed_objects_processor import SensedObjectsProcessor
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
        self._sensors_manager = DependencyContainer.sensors_manager()
        self._sensed_objects_schema = SensedObjectSchema(strict=True, many=True)
        self._serializer = Serializer(SensorSchema(strict=True))


class SensorListResource(AbstractSensorResource):
    """
    Resource related to sensors in the system
    """

    __metaclass__ = ABCMeta

    __custom_error_mappings = {
        'SensorAlreadyExistsException': {
            'code': 409,
            'message': lambda e: str(e)
        }
    }

    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings, **kwargs)

    def _do_get(self):
        return self._serializer.serialize(self._sensors_manager.get_all_sensors())

class SensorResource(AbstractSensorResource):
    """
    Resource related to one particular sensor in the system
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _do_get(self, sensor_id):
        return self._serializer.serialize(self._sensor_manager.get_sensor(sensor_id=sensor_id))

class AbstractOwnedSensorResource(AbstractSensorResource):
    """
    Abstract resource for all sensors that are owned by another object
    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def _do_get_processor(self) -> SensedObjectsProcessor:
        raise NotImplementedError



class OwnedSensorListResource(AbstractOwnedSensorResource):
    """
    Abstract resource for all endpoints related to sensors owned by another object
    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _do_get(self, owner_id: str):
        sensors = self._do_get_owner(owner_id).sensors.values()
        return self._serializer.serialize(sensors)

    def _do_post(self, owner_id: str):
        owner = self._do_get_owner(owner_id)
        sensor = self._serializer.deserialize(self._get_post_data_as_json())
        owner.add_sensor(id=sensor.id, sensor=sensor)
        return sensor

class OwnedSensorResource(AbstractOwnedSensorResource):
    """
    Abstract resource for endpoints refering to an specific sensor that is owned by another object
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__sensed_objects_schema = SensedObjectSchema(strict=True, many=True)

    def _do_get(self, owner_id:str, sensor_id:str):
        owner = self._do_get_owner(owner_id)
        return self._serializer.serialize(owner.sensors.get(sensor_id))

    def _do_put(self, owner_id: str, sensor_id: str):
        objects = self.__sensed_objects_schema.load(self._get_post_data_as_json()).data
        try:
            self._do_get_processor().process_sensed_objects(owner_id=owner_id, sensor_id=sensor_id, sensed_objects=objects)
        except NotEnoughPointsException:
            pass