from abc import ABCMeta, abstractmethod

from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource

from src.resources.schemas.serializer import Serializer
from src.resources.schemas.signal_emitter_schema import SignalEmitterSchema

class AbstractSignalEmitterResource(AbstractResource):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._signal_emitters_manager = DependencyContainer.signal_emitters_manager()
        self._serializer = Serializer(SignalEmitterSchema(strict=True))

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
        return self._serializer.serialize(self._signal_emitters_manager.get_all_signal_emitters())

    def _do_post(self):
        signal_emitter = self._serializer.deserialize(self._get_post_data_as_json())
        return self._serializer.serialize(self._signal_emitters_manager.add_signal_emitter(signal_emitter_id=signal_emitter.id, signal_emitter=signal_emitter))


class SignalEmitterResource(AbstractSignalEmitterResource):
    """
    Resource related to one particular signal emitter in the system
    """

    def _do_get(self, signal_emitter_id):
        return self._serializer.serialize(self._signal_emitters_manager.get_signal_emitter(signal_emitter_id=signal_emitter_id))





