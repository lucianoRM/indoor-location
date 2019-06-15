from marshmallow import fields

from src.core.anchor.signal_emitting_anchor import SignalEmittingAnchor
from src.core.user.signal_emitting_user import SignalEmittingUser
from src.core.user.user import User
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.dict_field import DictField
from src.resources.schemas.typed_object_schema import TypedObjectSchema


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


class SignalEmitterSchema(TypedObjectSchema):

    __USER_TYPE = "USER"
    __ANCHOR_TYPE = "ANCHOR"

    signal = fields.Dict()

    def _get_valid_types(self):
        return [self.__USER_TYPE, self.__ANCHOR_TYPE]

    def _do_make_object(self, type, kwargs):
        if type == self.__USER_TYPE:
            return SignalEmittingUser(**kwargs)
        else:
            return SignalEmittingAnchor(**kwargs)

    def _get_object_type(self, original_object):
        if isinstance(original_object, User):
            return self.__USER_TYPE
        else:
            return self.__ANCHOR_TYPE





