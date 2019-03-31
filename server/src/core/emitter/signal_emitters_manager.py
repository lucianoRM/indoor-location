from abc import ABCMeta, abstractmethod
from typing import List

from src.core.emitter.signal_emitter import SignalEmitter


class SignalEmittersManager:
    """
    API for handling Signal Emitters
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_signal_emitter(self, signal_emitter_id: str, signal_emitter: SignalEmitter) -> SignalEmitter:
        """
        Add a new signal_emitter
        :param signal_emitter_id: the signal emitter_id
        :param signal_emitter: the signal emitter to add
        :raise SignalEmitterAlreadyExistsException: if the signal emitter was already added
        :return: the signal emitter added
        """
        raise NotImplementedError

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
    def remove_signal_emitter(self, signal_emitter_id: str) -> SignalEmitter:
        """
        Remove an signal emitter by id
        :param signal_emitter_id: The id to uniquely locate the signal emitter to remove
        :raise: UnknownSignalEmitterException: If the signal emitter is not found
        :return: The signal emitter with the given id
        """
        raise NotImplementedError

    @abstractmethod
    def update_signal_emitter(self, signal_emitter_id: str, signal_emitter: SignalEmitter) -> SignalEmitter:
        """
        Update an already existent signal emitter.
        :param signal_emitter_id: The id of the signal emitter to be updated
        :param signal_emitter: The new signal emitter that will replace the old one with new information
        :raise: UnknownSignalEmitterException if no signal emitter is found with the given id.
        :return: The new signal emitter updated
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