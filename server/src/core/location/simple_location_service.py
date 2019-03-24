from src.core.location.location_service import LocationService, LocationServiceException
from src.core.location.shape.circle import Circle


class SimpleLocationService(LocationService):
    """
    Simple implementation of a location service.
    """

    def locate_object(self, anchor_objects):
        """
        Computes the position of an object based on other static objects and sensed distances.
        For locating the object, all sensing data will first be sorted by timestamp in descending order.
        Every static object's position and sensing distance will define a circle with center = static object's position and radius = sensing_distance

        Then, we will compute the intersection between circles until it's empty. The position returned will be the center of the last polygon
        generated from circles intersections.

        :param anchor_objects: Other objects in range of the one being located and with an static position
        :return: approximate location of the sensed object
        """
        if len(anchor_objects) < 2:
            raise LocationServiceException("Not enough sensing points to locate object")

        sorted_anchor_objects = sorted(anchor_objects, key=lambda object: object.timestamp, reverse=True)
        final_location_area = self.__get_location_area_intersection(sorted_anchor_objects.pop(0), sorted_anchor_objects.pop(0))
        while(len(sorted_anchor_objects) != 0):
            next_anchor_object = sorted_anchor_objects.pop(0)
            location_area = Circle(center=next_anchor_object.position, radius=next_anchor_object.distance)
            location_area = final_location_area.intersection(location_area)
            if location_area.area == 0:
                break
            final_location_area = location_area
        if final_location_area.area == 0:
            raise LocationServiceException("Could not locate object with given data, areas don't intersect")
        return final_location_area.centroid

    def __get_location_area_intersection(self, sensed_object1, sensed_object2):
        circle1 = Circle(center=sensed_object1.position, radius=sensed_object1.distance)
        circle2 = Circle(center=sensed_object2.position, radius=sensed_object2.distance)
        return circle1.intersection(circle2)


class AnchorObject(object):
    """
    Simple class facilitate computing another object's location.
    This class should store only required information in order for the SimpleLocationService to work
    """

    def __init__(self,
                 position,
                 distance,
                 timestamp):
        """
        Create a new instance of an Anchor object
        :param position: The position of the object
        :param distance: The distance from that object
        :param timestamp: timestamp for when that distance was computed
        """
        self.position = position
        self.distance = distance
        self.timestamp = timestamp