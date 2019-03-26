from src.core.emitter.signal_emitter import SignalEmitter
from src.core.object.static_object import StaticObject


class StaticSignalEmitter(SignalEmitter, StaticObject):
    """
    A signal emitter that do not modify it's position within the system
    """

    def __init__(self, id, position, **kwargs):
        super(StaticSignalEmitter, self).__init__(id=id, position=position, **kwargs)