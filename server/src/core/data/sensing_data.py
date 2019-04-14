
class SensingData:
    """
    Class to model information being sensed from one sensor regarding one object. Information should be normalized
    in the units picked by the system.
    """

    def __init__(self, distance: float, timestamp: int):
        self.__distance = distance
        self.__timestamp = timestamp

    @property
    def distance(self) -> float:
        return self.__distance

    @property
    def timestamp(self) -> int:
        return self.__timestamp