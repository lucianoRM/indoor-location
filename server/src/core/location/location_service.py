from abc import ABCMeta
from typing import List, Tuple

from src.core.location.reference_point import ReferencePoint


class LocationService:
    """
    Abstract class to define a location service API.
    A location service should be responsible for computing an object's location given sensing information.
    """

    __metaclass__ = ABCMeta

    def locate_object(self, reference_points: List[ReferencePoint]) -> Tuple[float]:
        raise NotImplementedError


class LocationServiceException(Exception):
    """
    Base exception to raise from a location service.
    """
    pass

class NotEnoughPointsException(LocationServiceException):
    """
    There are not enough sensing points to properly locate the object
    """
    pass