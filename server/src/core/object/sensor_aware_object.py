from abc import abstractmethod, ABCMeta
from typing import Dict

from src.core.sensor.sensor import Sensor


class SensorAwareObject:
    """
    An object that knows about sensors
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, sensors: Dict[str, Sensor] = None, **kwargs):
        super().__init__(**kwargs)
        if not sensors:
            sensors = {}
        self.__sensors = sensors

    def add_sensor(self, id:str, sensor: Sensor):
        if id in self.__sensors:
            raise SensorAlreadyExistsException("The Sensor with id " + id + " was already registered")
        self.__sensors[id] = sensor

    @property
    def sensors(self) -> Dict[str, Sensor]:
        return self.__sensors


class SensorAlreadyExistsException(Exception):
    """
    Exception to be thrown if the Sensor being registered was already added in this object
    """
    pass