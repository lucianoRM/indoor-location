from src.core.emitter.signal_emitter import SignalEmitter
from src.core.object.sensor_aware_object import SensorAwareObject
from src.core.object.signal_emitter_aware_object import SignalEmitterAwareObject
from src.core.object.static_object import StaticObject
from src.core.sensor.sensor import Sensor


class Anchor(StaticObject, SensorAwareObject, SignalEmitterAwareObject):
    """
    Class to model anchors in the system. Anchors are static objects that don't modify its position.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_sensor(self, id: str) -> Sensor:
        sensor = super().get_sensor(id)
        sensor.position = self.position
        return sensor

    def get_signal_emitter(self, id: str) -> SignalEmitter:
        se = super().get_signal_emitter(id)
        se.position = self.position
        return se







