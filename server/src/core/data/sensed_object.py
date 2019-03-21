


class SensedObject(object):
    """
    Class to model an object being sensed by a sensor.
    Instances of this class should be immutable
    """

    def __init__(self, id, data):
        """
        Constructor for sensed object
        :param id: The id of the object sensed
        :param data: Data being sensed regarding that object
        """
        self.__id = id
        self.__data = data

    @property
    def id(self):
        return self.__id

    @property
    def data(self):
        return self.__data