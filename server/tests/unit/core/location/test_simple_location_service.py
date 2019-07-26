from _pytest.python_api import raises

from src.core.location.location_service import LocationServiceException
from src.core.location.reference_point import ReferencePoint
from src.core.location.simple_location_service import SimpleLocationService
from tests.unit.core.location.abstract_test_location_service import AbstractTestLocationService


class TestSimpleLocationService(AbstractTestLocationService):


    #ALL THIS IS KIND OF OUTDATED. THE SIMPLE LOCATION SERVICE SHOULD START EXPANDING ALL
    #CIRCLES UNTIL ALL INTERSECT AND TAKE THAT POINT AS LOCATION. THAT WAY, NOT INTERSECTING POINTS WILL NOT RAISE
    #ERRORS AND MORE CIRCLES SHOULD PROVIDE MORE PRECISION (I GUESS?)

    def get_impl(self):
        return SimpleLocationService()


    def test_not_intersecting_areas_raises_exception(self):
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
            )
        ]
        with raises(LocationServiceException):
            self._location_service.locate_object(reference_points=references)

    def test_extra_information_does_not_count_if_not_intersecting(self):
        references = [
            ReferencePoint(
                position=(0, 0),
                distance=3,
                timestamp=1
            ),
            ReferencePoint(
                position=(4, 0),
                distance=3,
                timestamp=1
            ),
            ReferencePoint(
                position=(10, 10),
                distance=1,
                timestamp=1
            )
        ]
        location_point = self._location_service.locate_object(reference_points=references)
        self._check_point(location_point, (2, 0))

    def test_uses_last_information(self):
        references = [
            ReferencePoint(
                position=(4, 0),
                distance=3,
                timestamp=2
            ),
            ReferencePoint(
                position=(10, 10),
                distance=1,
                timestamp=1
            ),
            ReferencePoint(
                position=(0, 0),
                distance=3,
                timestamp=5
            )
        ]
        location_point = self._location_service.locate_object(reference_points=references)
        self._check_point(location_point, (2, 0))