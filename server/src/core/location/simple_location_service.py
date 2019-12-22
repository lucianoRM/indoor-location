from typing import List

from src.core.location.location_service import LocationService, NotEnoughPointsException, LocationServiceException
from src.core.location.reference_point import ReferencePoint
from src.core.location.shape.circle import Circle


class SimpleLocationService(LocationService):
    """
    Simple implementation of a location service.
    """

    __INCREMENT_PERCENTAGE = 0.1  #10%
    __MAX_ITERATIONS = 10

    def __init__(self, logger):
        self.__logger = logger
        super().__init__()

    def locate_object(self, reference_points: List[ReferencePoint]) -> List[float]:
        """
        Computes the position of an object based on other static objects and sensed distances.
        Every static object's position and sensing distance will define a circle with center = static object's position and radius = sensing_distance

        Then, we will compute the intersection between all circles. If the don't all intersect, we will increase each radius until they all do.
        Then, compute the centroid of the intersection

        :param anchor_objects: Other objects in range of the one being located and with an static position
        :return: approximate location of the sensed object
        """
        if len(reference_points) < 2:
            raise NotEnoughPointsException("Not enough sensing points to locate object")

        percentage_increment = 0

        final_location_area = self.__get_intersection_polygon(reference_points, percentage_increment)
        it = 0
        while(final_location_area.area <= 0):
            percentage_increment += self.__INCREMENT_PERCENTAGE
            final_location_area = self.__get_intersection_polygon(reference_points, percentage_increment)
            it += 1
            if it > self.__MAX_ITERATIONS:
                raise LocationServiceException("Reached max number of iterations while locating point")

        self.__logger.info("SIMPLE - LOCATING OBJECT WITH " + str(len(reference_points)) + " REFERENCE POINTS, INC: " + str(percentage_increment))

        [self.__logger.info("x: " + str(rp.position[0]) + ", y: " + str(rp.position[1]) + ", dis: " + str(rp.distance)) for rp in reference_points]

        x = final_location_area.centroid.x
        y = final_location_area.centroid.y

        self.__logger.info("SIMPLE - Location done, x: " + str(x) + ", y: " + str(y))
        return [x, y]

    def __get_intersection_polygon(self, reference_points, percentage_increment):
        result_polygon = Circle(center=reference_points[0].position, radius=reference_points[0].distance * (1 + percentage_increment))
        for point in reference_points[1:]:
            intersection = result_polygon.intersection(Circle(center=point.position, radius=point.distance * (1 + percentage_increment)))
            if(intersection.area == 0):
                return intersection
            result_polygon = intersection
        return result_polygon