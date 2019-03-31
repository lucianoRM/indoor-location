from typing import List

from src.core.object.moving_object import MovingObject
from src.core.object.moving_objects_manager import  MovingObjectAlreadyExistsException, UnknownMovingObjectException
from src.core.object.observable_moving_objects_manager import ObservableMovingObjectsManager
from src.core.object.observable_static_objects_manager import ObservableStaticObjectsManager
from src.core.object.static_object import StaticObject
from src.core.object.static_objects_manager import  StaticObjectAlreadyExistsException, UnknownStaticObjectException
from src.core.sensor.sensor import Sensor
from src.core.sensor.sensors_manager import SensorsManager, SensorAlreadyExistsException, UnknownSensorException


class DefaultSensorsManager(SensorsManager):
    """Sensor manager"""

    def __init__(self,
                 moving_objects_manager: ObservableMovingObjectsManager,
                 static_objects_manager: ObservableStaticObjectsManager):
        """
        Constructor for Manager.
        :param moving_objects_manager: manager that handles moving sensors
        :param static_objects_manager: manager that handles static sensors
        """
        self.__moving_sensors = set()
        self.__static_sensors = set()

        self.__moving_objects_manager = moving_objects_manager
        self.__moving_objects_manager.call_on_add(self.__on_new_moving_sensor)
        self.__moving_objects_manager.call_on_remove(self.__on_moving_sensor_removed)

        self.__static_objects_manager = static_objects_manager
        self.__static_objects_manager.call_on_add(self.__on_new_static_sensor)
        self.__static_objects_manager.call_on_remove(self.__on_static_sensor_removed)

    def __on_new_static_sensor(self, sensor_id: str):
        self.__static_sensors.add(sensor_id)

    def __on_new_moving_sensor(self, sensor_id: str):
        self.__moving_sensors.add(sensor_id)

    def __on_static_sensor_removed(self, sensor_id: str):
        self.__static_sensors.remove(sensor_id)

    def __on_moving_sensor_removed(self, sensor_id: str):
        self.__moving_sensors.remove(sensor_id)

    def add_sensor(self, sensor_id: str, sensor: Sensor) -> Sensor:
        return_value = None
        try:
            if isinstance(sensor, StaticObject):
                return_value = self.__static_objects_manager.add_static_object(object_id=sensor_id, object=sensor)
                self.__static_sensors.add(sensor_id)
            elif isinstance(sensor, MovingObject):
                return_value = self.__moving_objects_manager.add_moving_object(object_id=sensor_id, object=sensor)
                self.__moving_sensors.add(sensor_id)
            return return_value
        except (StaticObjectAlreadyExistsException, MovingObjectAlreadyExistsException):
            raise SensorAlreadyExistsException("Sensor with id: " + sensor_id + " was already registered")

    def get_sensor(self, sensor_id: str) -> Sensor:
        try:
            if sensor_id in self.__moving_sensors:
                return self.__moving_objects_manager.get_moving_object(object_id=sensor_id)
            elif sensor_id in self.__static_sensors:
                return self.__static_objects_manager.get_static_object(object_id=sensor_id)
        except UnknownStaticObjectException:
            self.__static_sensors.remove(sensor_id)
        except UnknownMovingObjectException:
            self.__moving_sensors.remove(sensor_id)
        raise UnknownSensorException("A sensor with id: " + sensor_id + " does not exist")

    def update_sensor(self, sensor_id: str, sensor: Sensor) -> Sensor:
        try:
            if sensor_id in self.__moving_sensors:
                return self.__moving_objects_manager.update_moving_object(object_id=sensor_id, object=sensor)
            elif sensor_id in self.__static_sensors:
                return self.__static_objects_manager.update_static_object(object_id=sensor_id, object=sensor)
        except UnknownStaticObjectException:
            self.__static_sensors.remove(sensor_id)
        except UnknownMovingObjectException:
            self.__moving_sensors.remove(sensor_id)
        raise UnknownSensorException("A sensor with id: " + sensor_id + " does not exist")

    def remove_sensor(self, sensor_id: str) -> Sensor:
        try:
            if sensor_id in self.__moving_sensors:
                self.__moving_sensors.remove(sensor_id)
                return self.__moving_objects_manager.remove_moving_object(object_id=sensor_id)
            elif sensor_id in self.__static_sensors:
                self.__static_sensors.remove(sensor_id)
                return self.__static_objects_manager.remove_static_object(object_id=sensor_id)
        except (UnknownMovingObjectException,UnknownStaticObjectException):
            pass
        raise UnknownSensorException("A sensor with id: " + sensor_id + " does not exist")

    def get_all_sensors(self) -> List[Sensor]:
        all_sensors = []
        for id in self.__moving_sensors:
            all_sensors.append(self.__moving_objects_manager.get_moving_object(object_id=id))
        for id in self.__static_sensors:
            all_sensors.append(self.__static_objects_manager.get_static_object(object_id=id))
        return all_sensors
