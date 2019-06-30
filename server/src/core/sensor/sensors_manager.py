from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, List

from src.core.sensor.sensor import Sensor

T = TypeVar('T', bound=Sensor)

class SensorsManager:
    """
    API for handling Sensors
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def get_sensor(self, sensor_id: str) -> T:
        """
        Get a sensor by id
        :param sensor_id: the unique id of the sensor to get
        :raise UnknownSensorException: if a sensor with that id does not exist
        :return: the sensor retrieved
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_sensors(self) -> List[T]:
        """
        Return all registered sensors
        :return: all sensors
        """
        raise NotImplementedError


class SensorManagerException(Exception):
    """
    Root exception related to an SensorManager
    """


class SensorAlreadyExistsException(SensorManagerException):
    """
    Throw this exception when wanting to add a sensor that already exists
    """
    pass


class UnknownSensorException(SensorManagerException):
    """
    Throw this exception when the requested sensor is not found
    """
    pass