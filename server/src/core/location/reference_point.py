from typing import Tuple


class ReferencePoint:
    """
    Simple class to facilitate computing another object's location. It represents a fixed point of reference from the
    object being located.
    """

    def __init__(self,
                 position: Tuple[float, ...],
                 distance: float,
                 timestamp: int):
        """
        Create a new instance of an ReferencePoint object
        :param position: The fixed position of the object
        :param distance: The distance from that object
        :param timestamp: timestamp for when that distance was computed
        """
        self.__position = position
        self.__distance = distance
        self.__timestamp = timestamp

    @property
    def position(self):
        return self.__position

    @property
    def distance(self):
        return self.__distance

    @property
    def timestamp(self):
        return self.__timestamp