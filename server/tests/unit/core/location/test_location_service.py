from pytest import fixture, raises

from src.core.location.location_service import LocationServiceException
from src.core.location.simple_location_service import SimpleLocationService, Anchor


class TestLocationService:

    @fixture(autouse=True)
    def setUp(self):
        self.__location_service = SimpleLocationService()

    def __check_point(self, point, expected_coordinates, allowed_error=0.01):
        assert abs(point[0] - expected_coordinates[0]) < allowed_error
        assert abs(point[1] - expected_coordinates[1]) < allowed_error

    def test_with_no_data_raises_exception(self):
        with raises(LocationServiceException):
            self.__location_service.locate_object(anchors=[])

    def test_single_data_point_raises_exception(self):
        anchor_objects = [
            Anchor(
                position=(1, 1),
                distance=1,
                timestamp=1
            )
        ]
        with raises(LocationServiceException):
            self.__location_service.locate_object(anchors=anchor_objects)

    def test_not_intersecting_areas_raises_exception(self):
        anchor_objects = [
            Anchor(
                position=(0, 0),
                distance=1,
                timestamp=1
            ),
            Anchor(
                position=(2, 2),
                distance=1,
                timestamp=1
            )
        ]
        with raises(LocationServiceException):
            self.__location_service.locate_object(anchors=anchor_objects)

    def test_simple_intersection(self):
        anchor_objects = [
            Anchor(
                position=(0, 0),
                distance=3,
                timestamp=1
            ),
            Anchor(
                position=(4, 0),
                distance=3,
                timestamp=1
            )
        ]
        location_point = self.__location_service.locate_object(anchors=anchor_objects)
        self.__check_point(location_point, (2, 0))

    def test_extra_information_does_not_count_if_not_intersecting(self):
        anchor_objects = [
            Anchor(
                position=(0, 0),
                distance=3,
                timestamp=1
            ),
            Anchor(
                position=(4, 0),
                distance=3,
                timestamp=1
            ),
            Anchor(
                position=(10, 10),
                distance=1,
                timestamp=1
            )
        ]
        location_point = self.__location_service.locate_object(anchors=anchor_objects)
        self.__check_point(location_point, (2, 0))

    def test_uses_last_information(self):
        anchor_objects = [
            Anchor(
                position=(4, 0),
                distance=3,
                timestamp=2
            ),
            Anchor(
                position=(10, 10),
                distance=1,
                timestamp=1
            ),
            Anchor(
                position=(0, 0),
                distance=3,
                timestamp=5
            )
        ]
        location_point = self.__location_service.locate_object(anchors=anchor_objects)
        self.__check_point(location_point, (2, 0))
