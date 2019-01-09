from src.core.exception.exceptions import IllegalArgumentException


class Sensor:
    """
    Stores all information related to a sensor that is part of the system
    """

    def __init__(self, **kwargs):
        """
        Constructor for Sensor.  It receives keyworded arguments to simulate a builder pattern.
        Only mandatory parameters will be validated. Otherwise, a default value will be used.
        :raises IllegalArgumentException: If mandatory arguments are not present
        :param kwargs: arguments to build the sensor
        """
        self.name = kwargs.get(self.NAME_KEY)
        self.id = kwargs.get(self.ID_KEY, self.__generate_uuid())
        self.location = kwargs.get(self.LOCATION_KEY, self.__generate_starting_location())
        if not self.name:
            raise IllegalArgumentException("Sensor must define a name")

        def __generate_uuid(self):
            return uuid4()