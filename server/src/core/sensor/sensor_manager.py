from abc import ABCMeta, abstractmethod


class SensorManager(object):
    """
    API for handling Sensors
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_sensor(self, sensor_id, sensor):
        """
        Add a new sensor
        :param sensor_id: the sensor_id
        :param sensor: the sensor to add
        :raise SensorAlreadyExistsException: if the sensor was already added
        :return: the sensor added
        """
        raise NotImplementedError

    @abstractmethod
    def get_sensor(self, sensor_id):
        """
        Get a sensor by id
        :param sensor_id: the unique id of the sensor to get
        :raise UnknownSensorException: if a sensor with that id does not exist
        :return: the sensor retrieved
        """
        raise NotImplementedError

    @abstractmethod
    def remove_sensor(self, sensor_id):
        """
        Remove an sensor by id
        :param sensor_id: The id to uniquely locate the sensor to remove
        :raise: UnkownSensorException: If the sensor is not found
        :return: The sensor with the given id
        """
        raise NotImplementedError

    @abstractmethod
    def update_sensor(self, sensor_id, sensor):
        """
        Update an already existent sensor.
        :param sensor_id: The id of the sensor to be updated
        :param sensor: The new sensor that will replace the old one with new information
        :raise: UnknownSensorException if no sensor is found with the given id.
        :return: The new sensor updated
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_sensors(self):
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