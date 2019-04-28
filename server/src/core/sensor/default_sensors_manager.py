from typing import List

from src.core.manager.default_positionable_objects_manager import PositionableObjectsManagerObserver
from src.core.manager.positionable_objects_manager import ObjectAlreadyExistsException, UnknownObjectException
from src.core.sensor.sensor import Sensor
from src.core.sensor.sensors_manager import SensorsManager, SensorAlreadyExistsException, UnknownSensorException


class DefaultSensorsManager(SensorsManager):
    """Sensor manager"""

    def __init__(self, objects_manager: PositionableObjectsManagerObserver):
        """
        Constructor for Manager.
        :param objects_manager: manager that handles sensors
        """
        super().__init__()
        self.__objects_manager = objects_manager
        self.__objects_manager.accepted_types = [Sensor]


    def add_sensor(self, sensor_id: str, sensor: Sensor) -> Sensor:
        try:
            return self.__objects_manager.add_object(object_id=sensor_id, object=sensor)
        except ObjectAlreadyExistsException:
            raise SensorAlreadyExistsException("Sensor with id: " + sensor_id + " was already registered")

    def get_sensor(self, sensor_id: str) -> Sensor:
        try:
            return self.__objects_manager.get_object(object_id=sensor_id)
        except UnknownObjectException:
            pass
        raise UnknownSensorException("A sensor with id: " + sensor_id + " does not exist")

    def update_sensor(self, sensor_id: str, sensor: Sensor) -> Sensor:
        try:
            return self.__objects_manager.update_object(object_id=sensor_id, object=sensor)
        except UnknownObjectException:
            raise UnknownSensorException("A sensor with id: " + sensor_id + " does not exist")

    def remove_sensor(self, sensor_id: str) -> Sensor:
        try:
            return self.__objects_manager.remove_object(object_id=sensor_id)
        except UnknownObjectException:
            raise UnknownSensorException("A sensor with id: " + sensor_id + " does not exist")

    def get_all_sensors(self) -> List[Sensor]:
        return self.__objects_manager.get_all_objects()
