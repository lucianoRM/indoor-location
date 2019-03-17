


class SensedObject(object):
    """
    Class to model an object being sensed by a sensor.
    Instances of this class should be immutable
    """

    def __init__(self, object_id, data):
        """
        Constructor for sensed object
        :param object_id: The id of the object sensed
        :param data: Data being sensed regarding that object
        """
        self.__object_id = object_id
        self.__data = data

    @property
    def object_id(self):
        return self.__object_id

    @property
    def data(self):
        return self.__data