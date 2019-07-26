from typing import List

from src.core.location.location_service import LocationService, LocationServiceException, NotEnoughPointsException
from src.core.location.reference_point import ReferencePoint
from src.core.location.shape.circle import Circle


class SimpleLocationService(LocationService):
    """
    Simple implementation of a location service.
    """

    def locate_object(self, reference_points: List[ReferencePoint]) -> List[float]:
        """
        Computes the position of an object based on other static objects and sensed distances.
        For locating the object, all sensing data will first be sorted by timestamp in descending order.
        Every static object's position and sensing distance will define a circle with center = static object's position and radius = sensing_distance

        Then, we will compute the intersection between circles until it's empty. The position returned will be the center of the last polygon
        generated from circles intersections.

        :param anchor_objects: Other objects in range of the one being located and with an static position
        :return: approximate location of the sensed object
        """
        if len(reference_points) < 2:
            raise NotEnoughPointsException("Not enough sensing points to locate object")

        sorted_rps = sorted(reference_points, key=lambda object: object.timestamp, reverse=True)
        final_location_area = self.__get_location_area_intersection(sorted_rps.pop(0), sorted_rps.pop(0))
        while(len(sorted_rps) != 0):
            next_rp = sorted_rps.pop(0)
            location_area = Circle(center=next_rp.position, radius=next_rp.distance)
            location_area = final_location_area.intersection(location_area)
            if location_area.area == 0:
                break
            final_location_area = location_area
        if final_location_area.area == 0:
            raise LocationServiceException("Could not locate object with given data, areas don't intersect")
        return [final_location_area.centroid.x, final_location_area.centroid.y]

    def __get_location_area_intersection(self, sensed_object1, sensed_object2):
        circle1 = Circle(center=sensed_object1.position, radius=sensed_object1.distance)
        circle2 = Circle(center=sensed_object2.position, radius=sensed_object2.distance)
        return circle1.intersection(circle2)
