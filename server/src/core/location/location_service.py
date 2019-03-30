from abc import ABCMeta

class LocationService:
    """
    Abstract class to define a location service API.
    A location service should be responsible for computing an object's location given sensing information.
    """

    __metaclass__ = ABCMeta

    def locate_object(self, sensed_objects):
        raise NotImplementedError






class LocationServiceException(Exception):
    """
    Base exception to raise from a location service.
    """