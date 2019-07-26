from abc import ABCMeta, abstractmethod

from pytest import fixture, raises

from src.core.location.location_service import LocationServiceException
from src.core.location.reference_point import ReferencePoint

class AbstractTestLocationService:

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_impl(self):
        raise NotImplementedError()

    @fixture(autouse=True)
    def setUp(self):
        self._location_service = self.get_impl()

    def _check_point(self, point, expected_coordinates, allowed_error=0.01):
        assert abs(point[0] - expected_coordinates[0]) < allowed_error
        assert abs(point[1] - expected_coordinates[1]) < allowed_error

    def test_with_no_data_raises_exception(self):
        with raises(LocationServiceException):
            self._location_service.locate_object(reference_points=[])

    def test_single_data_point_raises_exception(self):
        references = [
            ReferencePoint(
                position=(1, 1),
                distance=1,
                timestamp=1
            )
        ]
        with raises(LocationServiceException):
            self._location_service.locate_object(reference_points=references)

    def test_simple_intersection(self):
        references = [
            ReferencePoint(
                position=(0, 0),
                distance=2,
                timestamp=1
            ),
            ReferencePoint(
                position=(4, 0),
                distance=2,
                timestamp=1
            )
        ]
        location_point = self._location_service.locate_object(reference_points=references)
        self._check_point(location_point, (2, 0))

    def test_location_with_many_references(self):
        references = [
            ReferencePoint(
                position=(-1,0),
                distance=1,
                timestamp=1
            ),
            ReferencePoint(
                position=(1,0),
                distance=1,
                timestamp=1
            ),
            ReferencePoint(
                position=(0,-1),
                distance=1,
                timestamp=1
            ),
            ReferencePoint(
                position=(0,1),
                distance=1,
                timestamp=1
            )
        ]
        location_point = self._location_service.locate_object(reference_points=references)
        self._check_point(location_point, (0, 0))

