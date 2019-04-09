from src.core.data.sensing_data import SensingData

class SensedObject:
    """
    Class to model an object being sensed by a sensor.
    Instances of this class should be immutable
    """

    def __init__(self, sensor, id: str, data: SensingData):
        """
        Constructor for sensed object
        :param sensor: The sensor that sensed the object
        :param id: The id of the object sensed
        :param data: Data being sensed regarding that object
        """
        super().__init__()
        self.__sensor = sensor
        self.__id = id
        self.__data = data

    @property
    def sensor(self):
        return self.__sensor

    @property
    def id(self):
        return self.__id

    @property
    def data(self):
        return self.__data