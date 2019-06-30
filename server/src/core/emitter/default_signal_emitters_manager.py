from typing import List

from src.core.emitter.signal_emitter import SignalEmitter
from src.core.emitter.signal_emitters_manager import SignalEmittersManager, UnknownSignalEmitterException, \
    SignalEmitterAlreadyExistsException
from src.core.manager.default_positionable_objects_manager import PositionableObjectsManagerObserver
from src.core.manager.positionable_objects_manager import UnknownObjectException
from src.core.object.signal_emitter_aware_object import SignalEmitterAwareObject


class DefaultSignalEmittersManager(SignalEmittersManager):
    """Signal emitters manager"""

    def __init__(self, objects_manager: PositionableObjectsManagerObserver):
        """
        Constructor for Manager.
        :param objects_manager: manager that handles signal emitters
        """
        super().__init__()
        self.__index = {}
        self.__objects_manager = objects_manager
        self.__objects_manager.register_on_add_callback(self.__on_add)
        self.__objects_manager.register_on_remove_callback(self.__on_remove)

    def __on_add(self, owner_id: str, owner: SignalEmitterAwareObject):
        for se_id in owner.signal_emitters:
            if se_id in self.__index:
                raise SignalEmitterAlreadyExistsException(
                    "The signal emitter with id: " + se_id + "already exists in the system")
            self.__index[se_id] = owner_id

    def __on_remove(self, obj: SignalEmitterAwareObject):
        for se_id in obj.signal_emitters:
            self.__index.pop(se_id)

    def __get_owner(self, se_id: str) -> SignalEmitterAwareObject:
        owner_id = self.__index.get(se_id)
        owner = self.__objects_manager.get_object(object_id=owner_id)
        return owner

    def get_signal_emitter(self, signal_emitter_id: str) -> SignalEmitter:
        try:
            owner = self.__get_owner(signal_emitter_id)
            return owner.signal_emitters.get(signal_emitter_id)
        except (UnknownObjectException, KeyError):
            raise UnknownSignalEmitterException("A signal emitter with id: " + signal_emitter_id + " does not exist")

    def get_all_signal_emitters(self) -> List[SignalEmitter]:
        signal_emitters = []
        for se_id in self.__index:
            owner = self.__get_owner(se_id)
            for se in owner.signal_emitters.values():
                signal_emitters.append(se)
        return signal_emitters
