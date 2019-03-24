from unittest import TestCase
from src.core.location.location_service import LocationServiceException
from src.core.location.simple_location_service import SimpleLocationService, AnchorObject


class LocationServiceUnitTest(TestCase):

    def setUp(self):
        self.__location_service = SimpleLocationService()

    def __check_point(self, point, expected_coordinates, allowed_error = 0.01):
        self.assertTrue(abs(point.x - expected_coordinates[0]) < allowed_error)
        self.assertTrue(abs(point.y - expected_coordinates[1]) < allowed_error)



    def test_with_no_data_raises_exception(self):
        self.assertRaises(LocationServiceException, self.__location_service.locate_object, anchor_objects=[])

    def test_single_data_point_raises_exception(self):
        anchor_objects = [
            AnchorObject(
                position=(1,1),
                distance= 1,
                timestamp=1
            )
        ]
        self.assertRaises(LocationServiceException, self.__location_service.locate_object, anchor_objects=anchor_objects)

    def test_not_intersecting_areas_raises_exception(self):
        anchor_objects = [
            AnchorObject(
                position=(0, 0),
                distance=1,
                timestamp=1
            ),
            AnchorObject(
                position=(2, 2),
                distance=1,
                timestamp=1
            )
        ]
        self.assertRaises(LocationServiceException, self.__location_service.locate_object, anchor_objects=anchor_objects)

    def test_simple_intersection(self):
        anchor_objects = [
            AnchorObject(
                position=(0, 0),
                distance=3,
                timestamp=1
            ),
            AnchorObject(
                position=(4, 0),
                distance=3,
                timestamp=1
            )
        ]
        location_point = self.__location_service.locate_object(anchor_objects=anchor_objects)
        self.__check_point(location_point, (2,0))

    def test_extra_information_does_not_count_if_not_intersecting(self):
        anchor_objects = [
            AnchorObject(
                position=(0, 0),
                distance=3,
                timestamp=1
            ),
            AnchorObject(
                position=(4, 0),
                distance=3,
                timestamp=1
            ),
            AnchorObject(
                position=(10, 10),
                distance=1,
                timestamp=1
            )
        ]
        location_point = self.__location_service.locate_object(anchor_objects=anchor_objects)
        self.__check_point(location_point, (2, 0))


    def test_uses_last_information(self):
        anchor_objects = [
            AnchorObject(
                position=(4, 0),
                distance=3,
                timestamp=2
            ),
            AnchorObject(
                position=(10, 10),
                distance=1,
                timestamp=1
            ),
            AnchorObject(
                position=(0, 0),
                distance=3,
                timestamp=5
            )
        ]
        location_point = self.__location_service.locate_object(anchor_objects=anchor_objects)
        self.__check_point(location_point, (2, 0))
