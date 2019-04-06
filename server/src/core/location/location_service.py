from abc import ABCMeta
from typing import List, Tuple


class LocationService:
    """
    Abstract class to define a location service API.
    A location service should be responsible for computing an object's location given sensing information.
    """

    __metaclass__ = ABCMeta

    def locate_object(self, sensed_objects: List['AnchorObject']) -> Tuple[float]:
        raise NotImplementedError


class LocationServiceException(Exception):
    """
    Base exception to raise from a location service.
    """