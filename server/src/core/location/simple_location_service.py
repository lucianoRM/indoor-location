from src.core.location.location_service import LocationService, LocationServiceException
from src.core.location.shape.circle import Circle


class SimpleLocationService(LocationService):
    """
    Simple implementation of a location service.
    """

    def locate_object(self, sensed_objects):
        """
        For locating the object, all sensing data will first be sorted by timestamp in descending order.
        Every sensor position and sensing distance will define a circle with center = censor's position and radius = sensing_distance

        Then, we will compute the intersection between circles until it's empty. The position returned will be the center of the last polygon
        generated from circles intersections.

        :param sensed_objects:
        :return: approximate location of the sensed object
        """
        if len(sensed_objects) < 2:
            raise LocationServiceException("Not enough sensing points to locate object")

        sorted_sensed_objects = sorted(sensed_objects, key=lambda object: object.data.timestamp, reverse=True)
        final_sensing_area_intersection = self.__get_sensing_area_intersection(sorted_sensed_objects.pop(0), sorted_sensed_objects.pop(0))
        while(len(sorted_sensed_objects) != 0):
            next_sensed_object = sorted_sensed_objects.pop(0)
            sensor_sensing_area = Circle(center=next_sensed_object.sensor.position, radius=next_sensed_object.data.distance.m)
            sensor_sensing_area = final_sensing_area_intersection.intersection(sensor_sensing_area)
            if sensor_sensing_area.area == 0:
                break
            final_sensing_area_intersection = sensor_sensing_area
        if final_sensing_area_intersection.area == 0:
            raise LocationServiceException("Could not locate object with given data, areas don't intersect")
        return final_sensing_area_intersection.centroid

    def __get_sensing_area_intersection(self, sensed_object1, sensed_object2):
        circle1 = Circle(center=sensed_object1.sensor.position, radius=sensed_object1.data.distance.m)
        circle2 = Circle(center=sensed_object2.sensor.position, radius=sensed_object2.data.distance.m)
        return circle1.intersection(circle2)