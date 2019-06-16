from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.signal_emitter_schema import SignalEmitterSchema


class SignalEmitterListResource(AbstractResource):
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
        self.__signal_emitters_manager = DependencyContainer.signal_emitters_manager()
        self.__signal_emitters_schema = SignalEmitterSchema(many=True, strict=True)
        self.__signal_emitter_schema = SignalEmitterSchema(strict=True)

    def _do_get(self):
        return self.__signal_emitters_schema.dump(self.__signal_emitters_manager.get_all_signal_emitters())

    def _do_post(self):
        signal_emitter = self.__signal_emitter_schema.load(self._get_post_data_as_json()).data
        return self.__signal_emitter_schema.dump(self.__signal_emitters_manager.add_signal_emitter(signal_emitter_id=signal_emitter.id, signal_emitter=signal_emitter))


class SignalEmitterResource(AbstractResource):
    """
    Resource related to one particular signal emitter in the system
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__signal_emitters_manager = DependencyContainer.signal_emitters_manager()
        self.__signal_emitter_schema = SignalEmitterSchema(strict=True)

    def _do_get(self, signal_emitter_id):
        return self.__signal_emitter_schema.dump(self.__signal_emitters_manager.get_signal_emitter(signal_emitter_id=signal_emitter_id))





