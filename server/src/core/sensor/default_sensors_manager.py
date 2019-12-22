from typing import List

from src.core.manager.default_positionable_objects_manager import PositionableObjectsManagerObserver
from src.core.manager.observable_objects_manager import Callback
from src.core.manager.positionable_objects_manager import UnknownObjectException
from src.core.object.sensor_aware_object import SensorAwareObject
from src.core.sensor.sensor import Sensor
from src.core.sensor.sensors_manager import SensorsManager, UnknownSensorException, SensorAlreadyExistsException


class DefaultSensorsManager(SensorsManager):
    """Sensor manager"""

    def __init__(self, objects_manager: PositionableObjectsManagerObserver):
        """
        Constructor for Manager.
        :param objects_manager: manager that handles sensors
        """
        super().__init__()
        self.__index = {}
        self.__objects_manager = objects_manager
        self.__objects_manager.register_on_add_callback(Callback(self.__on_add, self.__on_remove))
        self.__objects_manager.register_on_remove_callback(Callback(self.__on_remove, self.__on_add))
        self.__objects_manager.register_on_update_callback(Callback(self.__on_update, self.__fix_update))

    def __on_add(self, owner_id: str, owner: SensorAwareObject):
        for s_id in owner.sensors:
            if s_id in self.__index:
                raise SensorAlreadyExistsException(
                    "The sensor with id: " + s_id + " already exists in the system")
            self.__index[s_id] = owner_id

    def __on_remove(self, owner_id: str, owner: SensorAwareObject):
        for s_id in owner.sensors:
            self.__index.pop(s_id)

    def __on_update(self, owner_id: str, owner: SensorAwareObject, old_owner: SensorAwareObject):
        self.__on_remove(owner_id, old_owner)
        self.__on_add(owner_id, owner)

    def __fix_update(self, owner_id: str, owner: SensorAwareObject, old_owner: SensorAwareObject):
        self.__on_remove(owner_id, owner)
        self.__on_add(owner_id, old_owner)

    def get_owner(self, s_id: str) -> SensorAwareObject:
        try:
            owner_id = self.__index[s_id]
            owner = self.__objects_manager.get_object(object_id=owner_id)
            return owner
        except (UnknownObjectException, KeyError):
            raise UnknownSensorException("A sensor with id: " + s_id + " does not exist")

    def get_sensor(self, sensor_id: str) -> Sensor:
        owner = self.get_owner(sensor_id)
        return owner.get_sensor(sensor_id)


    def get_all_sensors(self) -> List[Sensor]:
        sensors = []
        for s_id in self.__index:
            owner = self.get_owner(s_id)
            for s in owner.sensors.values():
                sensors.append(s)
        return sensors
