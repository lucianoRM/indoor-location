import itertools
from typing import List, Tuple

from sympy import Point

from src.core.location.location_service import LocationService, NotEnoughPointsException
from src.core.location.reference_point import ReferencePoint


class GeometricLocationService(LocationService):
    """
    Location service implementation
    """
    __NO_INTERSECTION = "NO_INTERSECTION"
    __CONTAINED = "CONTAINED"

    __INCREMENT = 0.5
    __INCREMENT_PERCENTAGE = 0.1

    def __init__(self, logger):
        self.__logger = logger
        super().__init__()

    def locate_object(self, reference_points: List[ReferencePoint]) -> Tuple[float, ...]:
        if len(reference_points) < 3:
            raise NotEnoughPointsException("Not enough sensing points to locate object")

        # for all groups of 3
        combinations = itertools.combinations(reference_points, 3)

        total_points = 0
        x_accumm = 0
        y_accumm = 0

        self.__logger.info("GEOMETRIC - LOCATING OBJECT WITH " + str(len(reference_points)) + " REFERENCE POINTS")

        [self.__logger.info("x: " + str(rp.position[0]) + ", y: " + str(rp.position[1]) + ", dis: " + str(rp.distance))
         for rp in reference_points]

        for combination in list(combinations):
            result = self.__process_group(combination)
            total_points += len(result)
            for p in result:
                x_accumm += p.x
                y_accumm += p.y

        x = float(x_accumm * 1.0 / total_points)
        y = float(y_accumm * 1.0 / total_points)

        self.__logger.info("GEOMETRIC: Location done, x: " + str(x) + ", y: " + str(y))
        return x,y


    def __process_group(self, group: Tuple[ReferencePoint]) -> Tuple[Point, ...]:
        c1 = Point(group[0].position[0], group[0].position[1], evaluate=False)
        r1 = group[0].distance
        c2 = Point(group[1].position[0], group[1].position[1], evaluate=False)
        r2 = group[1].distance
        c3 = Point(group[2].position[0], group[2].position[1], evaluate=False)
        r3 = group[2].distance
        return (
            self.__find_point(c1, r1, c2, r2, c3).evalf(prec=2),
            self.__find_point(c1, r1, c3, r3, c2).evalf(prec=2),
            self.__find_point(c2, r2, c3, r3, c1).evalf(prec=2)
        )

    def __find_point(self, center1: Point, r1, center2: Point, r2, center3: Point):
        result = self.__find_intersection_points(center1, r1, center2, r2)
        if isinstance(result, str):
            if result is self.__NO_INTERSECTION:
                # increment both proportionally
                r1 += r1 * self.__INCREMENT_PERCENTAGE
                r2 += r2 * self.__INCREMENT_PERCENTAGE
                return self.__find_point(center1,
                                         r1,
                                         center2,
                                         r2,
                                         center3)
            # one contains the other
            if r1 > r2:
                r1 -= self.__INCREMENT
                r2 += self.__INCREMENT
            else:
                r1 += self.__INCREMENT
                r2 -= self.__INCREMENT
            return self.__find_point(center1, r1, center2, r2, center3)
        if len(result) == 1:
            return result[0]
        p1 = result[0]
        p2 = result[1]
        if center3.distance(p1) < center3.distance(p2):
            return p1
        return p2

    def __find_intersection_points(self, c1: Point, r1, c2: Point, r2):
        centers_distance = c1.distance(c2)
        if centers_distance == 0:
            return self.__find_intersection_points(Point(c1[0] + 0.1, c1[1] + 0.1, evaluate=False),
                                                   r1,
                                                   Point(c2[0] - 0.1, c2[1] - 0.1, evaluate=False),
                                                   r2)
        if centers_distance > (r1 + r2):
            # circles too far apart
            return self.__NO_INTERSECTION
        if centers_distance < abs(r1 - r2):
            #one circle is inside the other
            return self.__CONTAINED

        a = ((r1 ** 2) - (r2 ** 2) + (centers_distance ** 2)) / (2 * centers_distance)

        h = ((r1 ** 2) - (a ** 2)) ** (1 / 2)  # square root

        intersection_center = c1 + ((c2 - c1) * a) / centers_distance

        x0 = intersection_center[0]
        y0 = intersection_center[1]

        if centers_distance == r1 + r2:
            # only one solution
            return intersection_center,

        x1 = c1[0]
        y1 = c1[1]

        x2 = c2[0]
        y2 = c2[1]

        x_off = (h * (x2 - x1)) / centers_distance
        y_off = (h * (y2 - y1)) / centers_distance

        x_a = x0 + y_off
        y_a = y0 - x_off

        x_b = x0 - y_off
        y_b = y0 + x_off

        return (Point(x_a, y_a, evaluate=False), Point(x_b, y_b, evaluate=False))
