from src.core.object.static_object import StaticObject
from src.core.sensor.sensor import Sensor


class StaticSensor(Sensor, StaticObject):
    """
    class to model all sensors that do not change it's position within the system.
    They should be used as anchors to compute all positions relative to theirs
    """
