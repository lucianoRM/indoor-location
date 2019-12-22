
class CoordinatesTransformer:
    '''
    Transforms coordinates to draw them correctly in the canvas
    '''

    def __init__(self,
                 min_origin_x,
                 max_origin_x,
                 min_origin_y,
                 max_origin_y,
                 min_target_x,
                 max_target_x,
                 min_target_y,
                 max_target_y):
        self.__min_origin_x = min_origin_x
        self.__max_origin_x = max_origin_x
        self.__min_origin_y = min_origin_y
        self.__max_origin_y = max_origin_y

        self.__min_target_x = min_target_x
        self.__max_target_x = max_target_x
        self.__min_target_y = min_target_y
        self.__max_target_y = max_target_y

    def transform_offset(self, x_off, y_off):
        return (self.__transform_x(x_off) - self.__transform_x(0),
                self.__transform_y(y_off) - self.__transform_y(0))


    def transform(self, x, y):
        return (self.__transform_x(x), self.__transform_y(y))


    def __transform_x(self, real_x):
        divisor = self.__max_origin_x - self.__min_origin_x
        slope = (self.__max_target_x - self.__min_target_x)/divisor
        offset = ((self.__max_origin_x * self.__min_target_x) - (self.__max_target_x * self.__min_origin_x))/divisor
        return (slope * real_x) + offset

    def __transform_y(self, real_y):
        divisor = self.__max_origin_y - self.__min_origin_y
        slope = (self.__max_target_y - self.__min_target_y) / divisor
        offset = ((self.__max_origin_y * self.__min_target_y) - (self.__max_target_y * self.__min_origin_y)) / divisor
        return (slope * real_y) + offset




