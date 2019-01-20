from src.core.exception.exceptions import IllegalArgumentException

NAME_KEY = "name"
ID_KEY = "id"
LOCATION_KEY = "location"

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
        self.name = kwargs.get(NAME_KEY)
        self.id = kwargs.get(ID_KEY)
        self.location = kwargs.get(LOCATION_KEY)
        if not self.name:
            raise IllegalArgumentException("Sensor must define a name")
        if not self.id:
            raise IllegalArgumentException("Sensor must define an id")
        if not self.location:
            raise IllegalArgumentException("Sensor must have a location")


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id and self.name == other.name and self.location == other.location
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)