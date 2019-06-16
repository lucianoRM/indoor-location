
from src.core.location.location_service import NotEnoughPointsException
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.sensed_object_schema import SensedObjectSchema
from src.resources.schemas.sensor_schema import SensorSchema

class SensorListResource(AbstractResource):
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
        super().__init__(custom_error_mappings=self.__custom_error_mappings,**kwargs)
        self.__sensor_manager = DependencyContainer.sensors_manager()
        self.__sensors_schema = SensorSchema(many=True, strict=True)
        self.__sensor_schema = SensorSchema(strict=True)

    def _do_get(self):
        return self.__sensors_schema.dump(self.__sensor_manager.get_all_sensors())

    def _do_post(self):
        sensor = self.__sensor_schema.load(self._get_post_data_as_json()).data
        return self.__sensor_schema.dump(self.__sensor_manager.add_sensor(sensor_id=sensor.id, sensor=sensor))


class SensorResource(AbstractResource):
    """
    Resource related to one particular sensor in the system
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__sensor_manager = DependencyContainer.sensors_manager()
        self.__sensor_schema = SensorSchema()

        self.__sensed_objects_processor = DependencyContainer.sensed_objects_processor()
        self.__sensed_objects_schema = SensedObjectSchema(strict=True, many=True)

    def _do_get(self, sensor_id):
        return self.__sensor_schema.dump(self.__sensor_manager.get_sensor(sensor_id=sensor_id))

    def _do_put(self, sensor_id):
        objects = self.__sensed_objects_schema.load(self._get_post_data_as_json()).data
        try:
            self.__sensed_objects_processor.process_sensed_objects(sensor_id=sensor_id, sensed_objects=objects)
        except NotEnoughPointsException:
            pass





