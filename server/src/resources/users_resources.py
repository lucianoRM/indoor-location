from abc import ABCMeta, abstractmethod

from src.core.user.sensing_user import SensingUser
from src.core.user.signal_emitting_user import SignalEmittingUser
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.sensing_user_schema import SensingUserSchema
from src.resources.schemas.sensor_schema import SENSOR_TYPE
from src.resources.schemas.signal_emitter_schema import SIGNAL_EMITTER_TYPE
from src.resources.schemas.signal_emitting_user_schema import SignalEmittingUserSchema
from src.resources.schemas.typed_object_serializer import SerializationContext, TypedObjectSerializer

class AbstractUserResource(AbstractResource):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._user_manager = DependencyContainer.users_manager()
        self._serializer = TypedObjectSerializer(contexts=[
            SerializationContext(type=SENSOR_TYPE, schema=SensingUserSchema(strict=True),
                                 klass=SensingUser),
            SerializationContext(type=SIGNAL_EMITTER_TYPE, schema=SignalEmittingUserSchema(strict=True),
                                 klass=SignalEmittingUser),
        ])

class UserListResource(AbstractUserResource):
    """
    Resource representing Users in the system
    """

    __custom_error_mappings = {
        'UserAlreadyExistsException': {
            'code': 409,
            'message': lambda e: str(e)
        }
    }

    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings, **kwargs)

    def _do_get(self):
        return self._serializer.dump(self._user_manager.get_all_users())

    def _do_post(self):
        user = self._serializer.load(self._get_post_data_as_json())
        return self._serializer.dump(self._user_manager.add_user(user_id=user.id, user=user))


class UserResource(AbstractUserResource):
    """
    Resource related to one user in particular in the system
    """

    def _do_get(self, user_id):
        return self._serializer.dump(self._user_manager.get_user(user_id=user_id))



