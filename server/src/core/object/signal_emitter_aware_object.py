from abc import ABCMeta
from typing import Dict

from src.core.emitter.signal_emitter import SignalEmitter


class SignalEmitterAwareObject:
    """
    An object that knows about signal emitters
    """

    __metaclass__ = ABCMeta

    def __init__(self, signal_emitters: Dict[str, SignalEmitter] = None, **kwargs):
        super().__init__(**kwargs)
        if not signal_emitters:
            signal_emitters = {}
        self.__signal_emitters = signal_emitters

    def add_signal_emitter(self, id: str, signal_emitter: SignalEmitter):
        if id in self.__signal_emitters:
            raise SignalEmitterAlreadyExistsException("The signal emitter with id " + id + " is already registered")
        self.__signal_emitters[id] = signal_emitter

    @property
    def signal_emitters(self) -> Dict[str, SignalEmitter]:
        return self.__signal_emitters


class SignalEmitterAlreadyExistsException(Exception):
    """
    Exception to be thrown if a signal emitter that is already registered is added again
    """
    pass