from unittest import mock

from _pytest.python_api import raises

from src.core.location.geometric_location_service import GeometricLocationService
from src.core.location.location_service import LocationServiceException
from src.core.location.reference_point import ReferencePoint
from src.core.location.simple_location_service import SimpleLocationService
from tests.unit.core.location.abstract_test_location_service import AbstractTestLocationService


class TestGeometricLocationService(AbstractTestLocationService):

    def get_impl(self):
        logger = mock.Mock()
        return GeometricLocationService(logger=logger)


    def test_not_intersecting_areas_expand(self):
        references = [
            ReferencePoint(
                position=(0, 0),
                distance=1,
                timestamp=1
            ),
            ReferencePoint(
                position=(2, 2),
                distance=1,
                timestamp=1
            ),
            ReferencePoint(
                position=(0, 2),
                distance=1,
                timestamp=1
            ),
            ReferencePoint(
                position=(2, 0),
                distance=1,
                timestamp=1
            ),


        ]
        location_point = self._location_service.locate_object(reference_points=references)
        self._check_point(location_point, (1, 1))

    def test_more_points(self):
        references = [
            ReferencePoint(
                position=(4, 0),
                distance=3,
                timestamp=2
            ),
            ReferencePoint(
                position=(0, 4),
                distance=3,
                timestamp=1
            ),
            ReferencePoint(
                position=(-4, 0),
                distance=3,
                timestamp=5
            ),
            ReferencePoint(
                position=(0, -4),
                distance=3,
                timestamp=5
            )
        ]
        location_point = self._location_service.locate_object(reference_points=references)
        self._check_point(location_point, (0, 0))

    def test_one_point_inside_the_other(self):
        references = [
            ReferencePoint(
                position=(0, 0),
                distance=4,
                timestamp=2
            ),
            ReferencePoint(
                position=(2, 0),
                distance=1,
                timestamp=1
            ),
            ReferencePoint(
                position=(2, 2),
                distance=1,
                timestamp=5
            )
        ]
        location_point = self._location_service.locate_object(reference_points=references)
        self._check_point(location_point, (2.92, 0.73))
