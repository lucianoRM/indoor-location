from abc import ABCMeta, abstractmethod
from typing import List

from src.core.emitter.signal_emitter import SignalEmitter


class SignalEmittersManager:
    """
    API for handling Signal Emitters
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def get_signal_emitter(self, signal_emitter_id: str):
        """
        Get a signal emitter by id
        :param signal_emitter_id: the unique id of the signal emitter to get
        :raise UnknownSignalEmitterException: if a signal emitter with that id does not exist
        :return: the signal emitter retrieved
        """
        raise NotImplementedError

    @abstractmethod
    def locate_signal_emitter(self, signal_emitter_id: str):
        """
        Get a signal emitter position by using the signal emitter id
        :param signal_emitter_id: the unique id of the signal emitter to get
        :raise UnknownSignalEmitterException: if a signal emitter with that id does not exist
        :return: the position for the signal emitter retrieved
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_signal_emitters(self) -> List[SignalEmitter]:
        """
        Return all registered signal emitters
        :return: all signal emitters
        """
        raise NotImplementedError


class SignalEmittersManagerException(Exception):
    """
    Root exception related to an SignalEmitterManager
    """


class SignalEmitterAlreadyExistsException(SignalEmittersManagerException):
    """
    Throw this exception when wanting to add a signal emitter that already exists
    """
    pass


class UnknownSignalEmitterException(SignalEmittersManagerException):
    """
    Throw this exception when the requested signal emitter is not found
    """
    pass