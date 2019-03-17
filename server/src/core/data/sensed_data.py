
class SensedData(object):
    """
    Class to model data being sensed from one sensor regarding one object
    """

    def __init__(self,distance):
        self.__distance = distance

    @property
    def distance(self):
        return self.__distance