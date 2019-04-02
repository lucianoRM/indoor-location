from typing import List

from src.core.emitter.signal_emitter import SignalEmitter
from src.core.emitter.signal_emitters_manager import SignalEmittersManager, SignalEmitterAlreadyExistsException, \
    UnknownSignalEmitterException
from src.core.manager.positionable_objects_manager import PositionableObjectsManager, ObjectAlreadyExistsException, \
    UnknownObjectException


class DefaultSignalEmittersManager(SignalEmittersManager):
    """Signal emitters manager"""

    def __init__(self, objects_manager: PositionableObjectsManager):
        """
        Constructor for Manager.
        :param objects_manager: manager that handles signal emitters
        """
        super().__init__()
        self.__objects_manager = objects_manager

    def add_signal_emitter(self, signal_emitter_id: str, signal_emitter: SignalEmitter) -> SignalEmitter:
        try:
            return self.__objects_manager.add_object(object_id=signal_emitter_id, object=signal_emitter)
        except ObjectAlreadyExistsException:
            raise SignalEmitterAlreadyExistsException("Signal emitter with id: " + signal_emitter_id + " was already registered")

    def get_signal_emitter(self, signal_emitter_id: str) -> SignalEmitter:
        try:
            return self.__objects_manager.get_object(object_id=signal_emitter_id)
        except UnknownObjectException:
            raise UnknownSignalEmitterException("A signal emitter with id: " + signal_emitter_id + " does not exist")

    def update_signal_emitter(self, signal_emitter_id: str, signal_emitter: SignalEmitter) -> SignalEmitter:
        try:
            return self.__objects_manager.update_object(object_id=signal_emitter_id, object=signal_emitter)
        except UnknownObjectException:
            raise UnknownSignalEmitterException("A signal emitter with id: " + signal_emitter_id + " does not exist")

    def remove_signal_emitter(self, signal_emitter_id: str) -> SignalEmitter:
        try:
            return self.__objects_manager.remove_object(object_id=signal_emitter_id)
        except UnknownObjectException:
            raise UnknownSignalEmitterException("A signal emitter with id: " + signal_emitter_id + " does not exist")

    def get_all_signal_emitters(self) -> List[SignalEmitter]:
        return self.__objects_manager.get_all_objects()
