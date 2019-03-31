from typing import List

from src.core.emitter.signal_emitter import SignalEmitter
from src.core.emitter.signal_emitters_manager import SignalEmittersManager, SignalEmitterAlreadyExistsException, \
    UnknownSignalEmitterException
from src.core.object.moving_object import MovingObject
from src.core.object.moving_objects_manager import MovingObjectsManager, MovingObjectAlreadyExistsException, \
    UnknownMovingObjectException
from src.core.object.static_object import StaticObject
from src.core.object.static_objects_manager import StaticObjectsManager, StaticObjectAlreadyExistsException, \
    UnknownStaticObjectException

class DefaultSignalEmittersManager(SignalEmittersManager):
    """Signal emitters manager"""

    def __init__(self,
                 moving_objects_manager: MovingObjectsManager,
                 static_objects_manager: StaticObjectsManager):
        """
        Constructor for Manager.
        :param moving_objects_manager: manager that handles moving signal emitters
        :param static_objects_manager: manager that handles static signal emitters
        """
        self.__moving_signal_emitters = set()
        self.__static_signal_emitters = set()

        self.__moving_objects_manager = moving_objects_manager
        self.__static_objects_manager = static_objects_manager

    def add_signal_emitter(self, signal_emitter_id: str, signal_emitter: SignalEmitter) -> SignalEmitter:
        return_value = None
        try:
            if isinstance(signal_emitter, StaticObject):
                return_value = self.__static_objects_manager.add_static_object(object_id=signal_emitter_id, object=signal_emitter)
                self.__static_signal_emitters.add(signal_emitter_id)
            elif isinstance(signal_emitter, MovingObject):
                return_value = self.__moving_objects_manager.add_moving_object(object_id=signal_emitter_id, object=signal_emitter)
                self.__moving_signal_emitters.add(signal_emitter_id)
            return return_value
        except (StaticObjectAlreadyExistsException, MovingObjectAlreadyExistsException):
            raise SignalEmitterAlreadyExistsException("Signal emitter with id: " + signal_emitter_id + " was already registered")

    def get_signal_emitter(self, signal_emitter_id: str) -> SignalEmitter:
        try:
            if signal_emitter_id in self.__moving_signal_emitters:
                return self.__moving_objects_manager.get_moving_object(object_id=signal_emitter_id)
            elif signal_emitter_id in self.__static_signal_emitters:
                return self.__static_objects_manager.get_static_object(object_id=signal_emitter_id)
        except UnknownStaticObjectException:
            self.__static_signal_emitters.remove(signal_emitter_id)
        except UnknownMovingObjectException:
            self.__moving_signal_emitters.remove(signal_emitter_id)
        raise UnknownSignalEmitterException("A signal emitter with id: " + signal_emitter_id + " does not exist")

    def update_signal_emitter(self, signal_emitter_id: str, signal_emitter: SignalEmitter) -> SignalEmitter:
        try:
            if signal_emitter_id in self.__moving_signal_emitters:
                return self.__moving_objects_manager.update_moving_object(object_id=signal_emitter_id, object=signal_emitter)
            elif signal_emitter_id in self.__static_signal_emitters:
                return self.__static_objects_manager.update_static_object(object_id=signal_emitter_id, object=signal_emitter)
        except UnknownStaticObjectException:
            self.__static_signal_emitters.remove(signal_emitter_id)
        except UnknownMovingObjectException:
            self.__moving_signal_emitters.remove(signal_emitter_id)
        raise UnknownSignalEmitterException("A signal emitter with id: " + signal_emitter_id + " does not exist")

    def remove_signal_emitter(self, signal_emitter_id: str) -> SignalEmitter:
        try:
            if signal_emitter_id in self.__moving_signal_emitters:
                self.__moving_signal_emitters.remove(signal_emitter_id)
                return self.__moving_objects_manager.remove_moving_object(object_id=signal_emitter_id)
            elif signal_emitter_id in self.__static_signal_emitters:
                self.__static_signal_emitters.remove(signal_emitter_id)
                return self.__static_objects_manager.remove_static_object(object_id=signal_emitter_id)
        except (UnknownMovingObjectException,UnknownStaticObjectException):
            pass
        raise UnknownSignalEmitterException("A signal emitter with id: " + signal_emitter_id + " does not exist")

    def get_all_signal_emitters(self) -> List[SignalEmitter]:
        all_signal_emitters = []
        for id in self.__moving_signal_emitters:
            all_signal_emitters.append(self.__moving_objects_manager.get_moving_object(object_id=id))
        for id in self.__static_signal_emitters:
            all_signal_emitters.append(self.__static_objects_manager.get_static_object(object_id=id))
        return all_signal_emitters
