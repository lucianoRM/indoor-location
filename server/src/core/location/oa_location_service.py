from typing import List, Tuple

from numpy.ma import array
from scipy.optimize import minimize

from src.core.location.location_service import LocationService, NotEnoughPointsException
from src.core.location.reference_point import ReferencePoint


class OALocationService(LocationService):
    """
    Location service that makes use of optimization algorithms to compute the position of an object given it's distance
    to other known anchors.
    """

    MAX_TOLERANCE = 1e-5
    MAX_ITERATIONS = 1000

    def __init__(self, logger):
        self.__logger = logger
        super().__init__()

    def locate_object(self, reference_points: List[ReferencePoint]) -> Tuple[float]:
        if len(reference_points) < 2:
            self.__logger.warning("NOT ENOUGH POINTS")
            raise NotEnoughPointsException("Not enough sensing points to locate object")

        self.__logger.info("OPTIMIZED - LOCATING OBJECT WITH " + str(len(reference_points)) + " REFERENCE POINTS")

        [self.__logger.info("x: " + str(rp.position[0]) + ", y: " + str(rp.position[1]) + ", dis: " + str(rp.distance)) for rp in reference_points]

        positions = [rp.position for rp in reference_points]
        distances = [rp.distance for rp in reference_points]

        result = minimize(
            self.__compute_square_error,
                self.__get_starting_point(reference_points),
                args=(positions, distances),
                method='L-BFGS-B',
                options={
                    'ftol':self.MAX_TOLERANCE,
                    'maxiter':self.MAX_ITERATIONS
                })

        computed_position = tuple(result.x)

        self.__logger.info("OPTIMIZED - Location done, x: " + str(computed_position[0]) + ", y: " + str(computed_position[1]))

        return computed_position

    def __compute_square_error(self, tmp_point, positions, distances):
        se = 0.0
        for i in range(len(positions)):
            measured_distance = distances[i]
            position = positions[i]
            computed_distance = ((tmp_point[0] - position[0])**2 + (tmp_point[1] - position[1])**2)**(1/2)
            se += (computed_distance - measured_distance)**2
        return se/len(positions)

    def __get_starting_point(self,reference_points: List[ReferencePoint]) -> Tuple[float]:
        points_array = array([r.position for r in reference_points])
        return points_array.mean(axis=0)




