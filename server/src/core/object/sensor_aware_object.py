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

    def add_sensor(self, id: str, sensor: Sensor):
        if id in self.__sensors:
            raise SensorAlreadyExistsException("The sensor with id: " + id + " already exists in the system")
        self.__sensors[id] = sensor

    def remove_sensor(self, id: str):
        try:
            self.__sensors.pop(id)
        except KeyError:
            raise UnknownSensorException("There is no sensor registered with id: " + id)

    def update_sensor(self, id: str, sensor: Sensor):
        if id not in self.__sensors:
            raise UnknownSensorException("There is no sensor registered with id: " + id)
        self.__sensors.update({id:sensor})

    @property
    def sensors(self) -> Dict[str, Sensor]:
        return self.__sensors


class SensorAwareObjectException(Exception):
    """
    Base exception raised by any SensorAwareObject
    """
    pass

class SensorAlreadyExistsException(SensorAwareObjectException):
    """
    Exception to be thrown if the Sensor being registered was already added in this object
    """
    pass

class UnknownSensorException(SensorAwareObjectException):
    """
    Exception to be raised when wanting to remove or update a sensor with an id that does not exist
    in this object
    """
    pass
