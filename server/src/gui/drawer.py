
class Drawer:
    '''
    Abstract class for an object that knows how to draw something in the canvas
    '''

    __TAG_SUFFIX = "-tag"

    def __init__(self, canvas, client, **kwargs):
        self._canvas = canvas
        self._client = client

    def draw(self, coordinates_transformer):
        '''
        make this Drawer update his drawings on the canvas
        '''
        raise NotImplementedError

    def _build_tag(self, base_id):
        return base_id.strip()

    def _build_label_tag(self, base_id):
        return self._build_tag(base_id) + self.__TAG_SUFFIX


