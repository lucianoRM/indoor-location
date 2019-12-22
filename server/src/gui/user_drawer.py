from tkinter import NW

from src.gui.color_generator import generate_hex_color
from src.gui.drawer import Drawer


class UserDrawer(Drawer):
    '''
    Drawer that knows how to draw users
    '''

    __CIRCLE_RADIUS = 6

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__drawn_users = {}

    def draw(self, coordinates_transformer):
        # collect offsets
        checked_ids = set([])
        server_users = self._client.get_users()
        for user in server_users:
            checked_ids.add(user.id)
            x = user.position[0]
            y = user.position[1]
            (t_x, t_y) = coordinates_transformer.transform(x, y)
            if user.id not in self.__drawn_users:
                tag = self._build_tag(user.id)
                label_tag = self._build_label_tag(user.id)
                drawn_user = DrawnUser(id=user.id,
                                       tag=tag,
                                       label_tag=label_tag,
                                       real_x=x,
                                       real_y=y,
                                       map_x=t_x,
                                       map_y=t_y)
                self.__drawn_users[user.id] = drawn_user
                self.__draw_new_user(drawn_user)
            else:
                drawn_user = self.__drawn_users[user.id]
                drawn_user.real_x = x
                drawn_user.real_y = y
                drawn_user.map_x = t_x
                drawn_user.map_y = t_y
                self.__move_user(drawn_user)

        # remove all users
        for user_id in self.__drawn_users:
            if user_id not in checked_ids:
                user = self.__drawn_users.pop(user_id)
                self._canvas.delete(user.tag)
                self._canvas.delete(user.label_tag)

    def __draw_new_user(self, drawn_user):
        left = drawn_user.map_x - self.__CIRCLE_RADIUS
        up = drawn_user.map_y - self.__CIRCLE_RADIUS
        right = drawn_user.map_x + self.__CIRCLE_RADIUS
        bottom = drawn_user.map_y + self.__CIRCLE_RADIUS
        self._canvas.create_text(right, bottom, text=drawn_user.id, anchor=NW, tag=drawn_user.label_tag)
        self._canvas.create_oval(
            left,
            up,
            right,
            bottom,
            tag=drawn_user.tag,
            fill=generate_hex_color(drawn_user.id)
        )

    def __move_user(self, drawn_user):
        left = drawn_user.map_x - self.__CIRCLE_RADIUS
        up = drawn_user.map_y - self.__CIRCLE_RADIUS
        right = drawn_user.map_x + self.__CIRCLE_RADIUS
        bottom = drawn_user.map_y + self.__CIRCLE_RADIUS
        self._canvas.coords(drawn_user.tag, left, up, right, bottom)
        self._canvas.coords(drawn_user.label_tag,
                            right,
                            bottom)


class DrawnUser:

    def __init__(self, id, tag, label_tag, real_x, real_y, map_x, map_y):
        self.id = id
        self.tag = tag
        self.label_tag = label_tag
        self.real_x = real_x
        self.real_y = real_y
        self.map_x = map_x
        self.map_y = map_y
