
class SensingData(object):
    """
    Class to model information being sensed from one sensor regarding one object
    """

    def __init__(self, distance, timestamp):
        self.__distance = distance
        self.__timestamp = timestamp

    @property
    def distance(self):
        return self.__distance

    @property
    def timestamp(self):
        return self.__timestamp