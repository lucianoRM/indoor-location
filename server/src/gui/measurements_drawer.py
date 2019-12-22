from src.gui.color_generator import generate_hex_color
from src.gui.drawer import Drawer


class MeasurementsDrawer(Drawer):


    def __init__(self, canvas, client, **kwargs):
        super().__init__(canvas, client, **kwargs)

    def __build_circle_tag(self, user_id, se_id):
        return self._build_tag(user_id) + self._build_tag(se_id)

    def draw(self, coordinates_transformer):
        users = self._client.get_users()
        for user in users:
            sensed_objects = user.attributes.get('sensed', {})
            for sensed_id in sensed_objects:

                sensed = sensed_objects[sensed_id]
                position = sensed['position']
                distance = sensed['distance']

                print("SENDED: " + str(sensed_id) + " at " + str(distance) + " meters")

                sensed_tag = self.__build_circle_tag(user.id, sensed_id)
                self._canvas.delete(sensed_tag)
                x = position[0]
                y = position[1]
                (x, y) = coordinates_transformer.transform(x, y)
                (x_rad, y_rad) = coordinates_transformer.transform(distance, distance)
                left = x - x_rad
                up = y - y_rad
                right = x + x_rad
                bottom = y + y_rad
                self._canvas.create_oval(
                    left,
                    up,
                    right,
                    bottom,
                    tag=sensed_tag,
                    fill=generate_hex_color(user.id),
                    stipple='gray25'
                )

