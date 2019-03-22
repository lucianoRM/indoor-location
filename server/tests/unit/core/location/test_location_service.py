from unittest import TestCase

from measurement.measures import Distance

from src.core.data.sensed_object import SensedObject
from src.core.data.sensing_data import SensingData
from src.core.location.location_service import LocationServiceException
from src.core.location.simple_location_service import SimpleLocationService
from src.core.sensor.sensor import Sensor


class LocationServiceUnitTest(TestCase):

    def setUp(self):
        self.__location_service = SimpleLocationService()

    def __check_point(self, point, expected_coordinates, allowed_error = 0.01):
        self.assertTrue(abs(point.x - expected_coordinates[0]) < allowed_error)
        self.assertTrue(abs(point.y - expected_coordinates[1]) < allowed_error)



    def test_with_no_data_raises_exception(self):
        self.assertRaises(LocationServiceException, self.__location_service.locate_object, sensed_objects=[])

    def test_single_data_point_raises_exception(self):
        sensed_objects = [
            SensedObject(
                sensor=Sensor(
                    id=1,
                    position=(1,1)
                ),
                id=1,
                data=SensingData(
                    distance=Distance(m=1),
                    timestamp=1
                )
            )
        ]
        self.assertRaises(LocationServiceException, self.__location_service.locate_object, sensed_objects=sensed_objects)

    def test_not_intersecting_areas_raises_exception(self):
        sensed_objects = [
            SensedObject(
                sensor=Sensor(
                    id=1,
                    position=(0,0)
                ),
                id=1,
                data=SensingData(
                    distance=Distance(m=1),
                    timestamp=1
                )
            ),
            SensedObject(
                sensor=Sensor(
                    id=2,
                    position=(2, 2)
                ),
                id=1,
                data=SensingData(
                    distance=Distance(m=1),
                    timestamp=1
                )
            )
        ]
        self.assertRaises(LocationServiceException, self.__location_service.locate_object, sensed_objects=sensed_objects)

    def test_simple_intersection(self):
        sensed_objects = [
            SensedObject(
                sensor=Sensor(
                    id=1,
                    position=(0, 0)
                ),
                id=1,
                data=SensingData(
                    distance=Distance(m=3),
                    timestamp=1
                )
            ),
            SensedObject(
                sensor=Sensor(
                    id=2,
                    position=(4, 0)
                ),
                id=1,
                data=SensingData(
                    distance=Distance(m=3),
                    timestamp=1
                )
            )
        ]
        location_point = self.__location_service.locate_object(sensed_objects=sensed_objects)
        self.__check_point(location_point, (2,0))

    def test_extra_information_does_not_count_if_not_intersecting(self):
        sensed_objects = [
            SensedObject(
                sensor=Sensor(
                    id=1,
                    position=(0, 0)
                ),
                id=1,
                data=SensingData(
                    distance=Distance(m=3),
                    timestamp=1
                )
            ),
            SensedObject(
                sensor=Sensor(
                    id=2,
                    position=(4, 0)
                ),
                id=1,
                data=SensingData(
                    distance=Distance(m=3),
                    timestamp=1
                )
            ),
            SensedObject(
                sensor=Sensor(
                    id=2,
                    position=(10, 10)
                ),
                id=1,
                data=SensingData(
                    distance=Distance(m=1),
                    timestamp=1
                )
            )
        ]
        location_point = self.__location_service.locate_object(sensed_objects=sensed_objects)
        self.__check_point(location_point, (2, 0))


    def test_uses_last_information(self):
        sensed_objects = [
            SensedObject(
                sensor=Sensor(
                    id=2,
                    position=(4, 0)
                ),
                id=1,
                data=SensingData(
                    distance=Distance(m=3),
                    timestamp=2
                )
            ),
            SensedObject(
                sensor=Sensor(
                    id=2,
                    position=(10, 10)
                ),
                id=1,
                data=SensingData(
                    distance=Distance(m=1),
                    timestamp=1
                )
            ),
            SensedObject(
                sensor=Sensor(
                    id=1,
                    position=(0, 0)
                ),
                id=1,
                data=SensingData(
                    distance=Distance(m=3),
                    timestamp=5
                )
            ),
        ]
        location_point = self.__location_service.locate_object(sensed_objects=sensed_objects)
        self.__check_point(location_point, (2, 0))
