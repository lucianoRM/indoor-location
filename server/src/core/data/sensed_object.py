


class SensedObject(object):
    """
    Class to model an object being sensed by a sensor.
    Instances of this class should be immutable
    """

    def __init__(self, object_id, distance):
        """
        Constructor for sensed object
        :param object_id: The id of the object sensed
        :param distance: The objects distance from the sensor
        """
        self.__object_id = object_id
        self.__distance = distance

    @property
    def object_id(self):
        return self.__object_id

    @property
    def distance(self):
        return self.__distance