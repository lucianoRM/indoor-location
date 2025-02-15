import time
from abc import ABCMeta, abstractmethod

from flask import request

from src.core.data.sensed_objects_processor import SensedObjectsProcessor
from src.core.location.location_service import NotEnoughPointsException
from src.dependency_container import DependencyContainer
from src.resources.abstract_owned_object_resource import AbstractOwnedObjectResource
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
        self._sensor_serializer = Serializer(SensorSchema(strict=True))


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
        return self._sensor_serializer.serialize(self._sensors_manager.get_all_sensors())

class SensorResource(AbstractSensorResource):
    """
    Resource related to one particular sensor in the system
    """

    __custom_error_mappings = {
        'UnknownSensorException': {
            'code': 404,
            'message': lambda e: str(e)
        }
    }

    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings, **kwargs)

    def _do_get(self, sensor_id):
        return self._sensor_serializer.serialize(self._sensors_manager.get_sensor(sensor_id=sensor_id))

class AbstractOwnedSensorResource(AbstractSensorResource, AbstractOwnedObjectResource):
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
        owner = self._do_get_owner(owner_id)
        sensors = list(owner.get_sensor(id) for id in owner.sensors_ids)
        return self._sensor_serializer.serialize(sensors)

    def _do_post(self, owner_id: str):
        owner = self._do_get_owner(owner_id)
        sensor = self._sensor_serializer.deserialize(self._get_post_data_as_json())
        owner.add_sensor(id=sensor.id, sensor=sensor)
        self._update_owner(owner_id=owner_id, owner=owner)
        return self._sensor_serializer.serialize(sensor)

class OwnedSensorResource(AbstractOwnedSensorResource):
    """
    Abstract resource for endpoints refering to an specific sensor that is owned by another object
    """
    __metaclass__ = ABCMeta

    __LOCATION_SERVICE_KEY = "location_service"

    __custom_error_mappings = {
        'UnknownSensorException': {
            'code': 404,
            'message': lambda e: str(e)
        },
        'UnknownLocationServiceException': {
            'code': 404,
            'message': lambda e: str(e)
        }
    }

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings)
        self.__sensed_objects_schema = SensedObjectSchema(strict=True, many=True)

    def _do_get(self, owner_id:str, sensor_id:str):
        owner = self._do_get_owner(owner_id)
        return self._sensor_serializer.serialize(owner.get_sensor(sensor_id))

    def _do_put(self, owner_id: str, sensor_id: str):
        location_service_key = request.args.get(self.__LOCATION_SERVICE_KEY)
        data = self._get_post_data_as_json()
        if not data:
            data = []
        objects = self.__sensed_objects_schema.load(data).data
        try:
            self._do_get_processor().process_sensed_objects(owner_id=owner_id, sensor_id=sensor_id, sensed_objects=objects, location_service=location_service_key)
        except NotEnoughPointsException:
            pass