from abc import ABCMeta, abstractmethod

from src.core.object.signal_emitter_aware_object import SignalEmitterAwareObject
from src.dependency_container import DependencyContainer
from src.resources.abstract_owned_object_resource import AbstractOwnedObjectResource
from src.resources.abstract_resource import AbstractResource

from src.resources.schemas.serializer import Serializer
from src.resources.schemas.signal_emitter_schema import SignalEmitterSchema

class AbstractSignalEmitterResource(AbstractResource):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._signal_emitters_manager = DependencyContainer.signal_emitters_manager()
        self._signal_emitter_serializer = Serializer(SignalEmitterSchema(strict=True))

class SignalEmitterListResource(AbstractSignalEmitterResource):
    """
    Resource related to signal emitters in the system
    """

    __custom_error_mappings = {
        'SignalEmitterAlreadyExistsException': {
            'code': 409,
            'message': lambda e: str(e)
        }
    }

    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings, **kwargs)

    def _do_get(self):
        return self._signal_emitter_serializer.serialize(self._signal_emitters_manager.get_all_signal_emitters())

    def _do_post(self):
        signal_emitter = self._signal_emitter_serializer.deserialize(self._get_post_data_as_json())
        return self._signal_emitter_serializer.serialize(self._signal_emitters_manager.add_signal_emitter(signal_emitter_id=signal_emitter.id, signal_emitter=signal_emitter))


class SignalEmitterResource(AbstractSignalEmitterResource):
    """
    Resource related to one particular signal emitter in the system
    """

    def _do_get(self, signal_emitter_id):
        return self._signal_emitter_serializer.serialize(self._signal_emitters_manager.get_signal_emitter(signal_emitter_id=signal_emitter_id))


class AbstractOwnedSignalEmitterResource(AbstractSignalEmitterResource, AbstractOwnedObjectResource):
    """
    Abstract resource for all signal emitters that are owned by another object
    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class OwnedSignalEmitterListResource(AbstractOwnedSignalEmitterResource):
    """
    Abstract resource for all endpoints related to signal emitters owned by another object
    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _do_get(self, owner_id: str):
        signal_emitters = list(self._do_get_owner(owner_id).signal_emitters.values())
        return self._signal_emitter_serializer.serialize(signal_emitters)

    def _do_post(self, owner_id: str):
        owner = self._do_get_owner(owner_id)
        signal_emitter = self._signal_emitter_serializer.deserialize(self._get_post_data_as_json())
        owner.add_signal_emitter(id=signal_emitter.id, signal_emitter=signal_emitter)
        self._update_owner(owner_id=owner_id, owner=owner)
        return self._signal_emitter_serializer.serialize(signal_emitter)

class OwnedSignalEmitterResource(AbstractOwnedSignalEmitterResource):
    """
    Abstract resource for endpoints refering to an specific signal emitter that is owned by another object
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _do_get(self, owner_id:str, signal_emitter_id:str):
        owner = self._do_get_owner(owner_id)
        return self._signal_emitter_serializer.serialize(owner.signal_emitters.get(signal_emitter_id))



