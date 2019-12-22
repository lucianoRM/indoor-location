from typing import Tuple

from shapely import affinity
from shapely.geometry import Point, Polygon


class Circle(Polygon):

    __NUMBER_OF_POINTS = 20

    def __get_polygon_points(self, center: Tuple[float], radius: float) -> Polygon:
        step_rotation_angle = 360/self.__NUMBER_OF_POINTS
        starting_point = Point(center[0] + radius, center[1])
        polygon_points = [(starting_point.x, starting_point.y)]
        rotated_point = starting_point
        for i in range(self.__NUMBER_OF_POINTS - 1):
            rotated_point = affinity.rotate(rotated_point, step_rotation_angle, origin=Point(center[0], center[1]))
            polygon_points.append((rotated_point.x, rotated_point.y))
        return Polygon(polygon_points)


    def __init__(self, center: Tuple[float], radius: float):
        self.__radius = radius
        super().__init__(shell=self.__get_polygon_points(center, radius))

    @property
    def radius(self):
        return self.__radius
