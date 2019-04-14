from typing import Tuple

from shapely.geometry import Point


class Position:
    """
    Defines a position of an object in the system
    """

    def __init__(self, x: float, y: float):
        self.__point = Point(x, y)

    @property
    def xy(self) -> Tuple[float]:
        return self.__point.xy()



