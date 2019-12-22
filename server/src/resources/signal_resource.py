from src.core.anchor.anchor import Anchor
from src.core.user.user import User
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource


class SignalResource(AbstractResource):

    __custom_error_mappings = {
        'UnknownAnchorException': {
            'code': 404,
            'message': lambda e: str(e)
        },
        'UnknownSensorException': {
            'code': 404,
            'message': lambda e: str(e)
        },
        'UnknownSignalEmitterException': {
            'code': 404,
            'message': lambda e: str(e)
        }
    }

    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings, **kwargs)
        self.__signal_emitter_manager = DependencyContainer.signal_emitters_manager()
        self.__anchor_manager = DependencyContainer.anchors_manager()
        self.__user_manager = DependencyContainer.users_manager()

    def _do_put(self, signal_emitter_id):
        owner = self.__signal_emitter_manager.get_owner(signal_emitter_id)
        signal_emitter = owner.get_signal_emitter(signal_emitter_id)
        new_signal = self._get_post_data_as_json()
        signal_emitter.signal.update(new_signal)
        owner.update_signal_emitter(signal_emitter_id, signal_emitter)
        if isinstance(owner, Anchor):
            self.__anchor_manager.update_anchor(owner.id, owner)
        elif isinstance(owner, User):
            self.__user_manager.update_user(owner.id, owner)
