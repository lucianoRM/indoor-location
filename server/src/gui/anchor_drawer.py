from tkinter import NW

from src.gui.drawer import Drawer


class AnchorDrawer(Drawer):
    '''
    Knows how to draw anchors in the canvas
    '''

    __ANCHOR_WIDTH_PX = 6
    __ANCHOR_HEIGHT_PX = 6
    __ANCHOR_COLOR = 'blue'

    def __init__(self, canvas, client, **kwargs):
        super().__init__(canvas, client, **kwargs)

    def draw(self, coordinates_transformer):
        anchors = self._client.get_anchors()
        for anchor in anchors:
            label_tag = self._build_label_tag(anchor.id)
            anchor_tag = self._build_tag(anchor.id)
            self._canvas.delete(anchor_tag)
            self._canvas.delete(label_tag)
            x = anchor.position[0]
            y = anchor.position[1]
            (x,y) = coordinates_transformer.transform(x,y)
            left = x - self.__ANCHOR_WIDTH_PX
            up = y - self.__ANCHOR_HEIGHT_PX
            right = x + self.__ANCHOR_WIDTH_PX
            bottom = y + self.__ANCHOR_HEIGHT_PX
            self._canvas.create_text(right, bottom, text=anchor.id, anchor=NW, tag=label_tag)
            self._canvas.create_rectangle(
                left,
                up,
                right,
                bottom,
                fill=self.__ANCHOR_COLOR,
                tag=anchor_tag
            )
