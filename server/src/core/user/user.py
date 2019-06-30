from src.core.object.moving_object import MovingObject
from src.core.object.sensor_aware_object import SensorAwareObject
from src.core.object.signal_emitter_aware_object import SignalEmitterAwareObject


class User(MovingObject, SensorAwareObject, SignalEmitterAwareObject):
    """
    Class that models an user using the system.
    An user should be any actor of the system that we want to locate.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
