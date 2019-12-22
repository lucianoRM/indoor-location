import tkinter

from src.gui.anchor_drawer import AnchorDrawer
from src.gui.client import Client
from src.gui.coordinates_transformer import CoordinatesTransformer
from src.gui.measurements_drawer import MeasurementsDrawer
from src.gui.user_drawer import UserDrawer


class App:
    __WIDTH_PX = 700
    __HEIGTH_PX = 700
    __EDGE_PX = 100

    __REFRESH_TIME = 500

    __DEFAULT_MAX_VALUE = 20
    __MAX_VALUE = 9999999

    def __init__(self, name='App'):
        self.__window = tkinter.Tk()
        self.__window.title(name)
        self.__canvas = tkinter.Canvas(self.__window,
                                       width=self.__WIDTH_PX,
                                       height=self.__HEIGTH_PX,
                                       highlightthickness=1,
                                       highlightbackground='black')
        self.__canvas.pack()
        self.__client = Client()
        self.__anchors_drawer = AnchorDrawer(canvas=self.__canvas, client=self.__client)
        self.__users_drawer = UserDrawer(canvas=self.__canvas, client=self.__client)
        self.__measurements_drawer = MeasurementsDrawer(canvas=self.__canvas, client=self.__client)
        self.__coordinates_transformer = None

    def start(self):
        self.__window.after(self.__REFRESH_TIME, self.__update)
        self.__window.mainloop()

    def on_stop(self, on_stop):
        self.__window.protocol("WM_DELETE_WINDOW",
                               lambda: on_stop() == self.__window.destroy())  # hack to run both functions

    def __update(self):
        self.__client.update()
        (min_origin_x, max_origin_x, min_origin_y, max_origin_y) = self.__get_edge_values(
            self.__client.get_anchors())
        min = min_origin_x if min_origin_x < min_origin_y else min_origin_y
        max = max_origin_x if max_origin_x > max_origin_y else max_origin_y
        self.__coordinates_transformer = CoordinatesTransformer(
            min_origin_x=min,
            max_origin_x=max,
            min_origin_y=min,
            max_origin_y=max,
            min_target_x=self.__EDGE_PX,
            max_target_x=self.__WIDTH_PX - self.__EDGE_PX,
            min_target_y=self.__EDGE_PX,
            max_target_y=self.__HEIGTH_PX - self.__EDGE_PX)

        self.__anchors_drawer.draw(self.__coordinates_transformer)
        self.__users_drawer.draw(self.__coordinates_transformer)
        # self.__measurements_drawer.draw(self.__coordinates_transformer)

        self.__window.after(self.__REFRESH_TIME, self.__update)

    def __get_edge_values(self, anchors):
        min_x = self.__MAX_VALUE
        min_y = self.__MAX_VALUE
        max_x = 0
        max_y = 0
        if len(anchors) == 0:
            return (0, self.__DEFAULT_MAX_VALUE, 0, self.__DEFAULT_MAX_VALUE)
        for anchor in anchors:
            x = anchor.position[0]
            y = anchor.position[1]
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
        if max_x == min_x:
            min_x = 0
        if max_y == min_y:
            min_y = 0
        if max_x == 0:
            max_x = self.__DEFAULT_MAX_VALUE
        if max_y == 0:
            max_y = self.__DEFAULT_MAX_VALUE
        return (min_x, max_x, min_y, max_y)
