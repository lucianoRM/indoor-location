from src.core.anchor.signal_emitting_anchor import SignalEmittingAnchor
from src.core.user.signal_emitting_user import SignalEmittingUser
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.anchor_schema import ANCHOR_TYPE
from src.resources.schemas.signal_emitting_anchor_schema import SignalEmittingAnchorSchema
from src.resources.schemas.signal_emitting_user_schema import SignalEmittingUserSchema
from src.resources.schemas.typed_object_serializer import SerializationContext, TypedObjectSerializer
from src.resources.schemas.user_schema import USER_TYPE


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

        contexts = [
            SerializationContext(type=ANCHOR_TYPE, schema=SignalEmittingAnchorSchema(strict=True),
                                 klass=SignalEmittingAnchor),
            SerializationContext(type=USER_TYPE, schema=SignalEmittingUserSchema(strict=True),
                                 klass=SignalEmittingUser),
        ]
        self.__signal_emitter_schema = TypedObjectSerializer(contexts=contexts)

    def _do_get(self):
        return self.__signal_emitter_schema.dump(self.__signal_emitters_manager.get_all_signal_emitters())

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
        contexts = [
            SerializationContext(type=ANCHOR_TYPE, schema=SignalEmittingAnchorSchema(strict=True), klass=SignalEmittingAnchor),
            SerializationContext(type=USER_TYPE, schema=SignalEmittingUserSchema(strict=True),
                                 klass=SignalEmittingUser),
        ]
        self.__signal_emitter_schema = TypedObjectSerializer(contexts=contexts)

    def _do_get(self, signal_emitter_id):
        return self.__signal_emitter_schema.dump(self.__signal_emitters_manager.get_signal_emitter(signal_emitter_id=signal_emitter_id))





