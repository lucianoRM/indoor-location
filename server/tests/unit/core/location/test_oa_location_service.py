from src.core.location.oa_location_service import OALocationService
from src.core.location.reference_point import ReferencePoint
from tests.unit.core.location.abstract_test_location_service import AbstractTestLocationService


class TestOALocationService(AbstractTestLocationService):

    def get_impl(self):
        return OALocationService()

    def test_location_with_not_intersecting_distances(self):
        references = [
            ReferencePoint(
                position=(-100, 0),
                distance=1,
                timestamp=1
            ),
            ReferencePoint(
                position=(100, 0),
                distance=50,
                timestamp=1
            )
        ]
        location_point = self._location_service.locate_object(reference_points=references)
        self._check_point(location_point, (-24.5, 0))
