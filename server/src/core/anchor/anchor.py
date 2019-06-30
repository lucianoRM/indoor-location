
from src.core.object.sensor_aware_object import SensorAwareObject
from src.core.object.signal_emitter_aware_object import SignalEmitterAwareObject
from src.core.object.static_object import StaticObject


class Anchor(StaticObject, SensorAwareObject, SignalEmitterAwareObject):
    """
    Class to model anchors in the system. Anchors are static objects that don't modify its position.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
