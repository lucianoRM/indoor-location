from src.core.anchor.anchor import Anchor
from src.core.sensor.sensor import Sensor


class SensingAnchor(Anchor, Sensor):
    """
    An anchor that is also a sensor
    """

    def __init__(self, id, position, **kwargs):
        super().__init__(id=id, position=position, **kwargs)