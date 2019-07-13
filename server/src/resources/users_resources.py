from abc import ABCMeta, abstractmethod

from src.core.data.sensed_objects_processor import SensedObjectsProcessor
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.serializer import Serializer
from src.resources.schemas.user_schema import UserSchema
from src.resources.sensors_resources import OwnedSensorListResource, OwnedSensorResource
from src.resources.signal_emitters_resources import OwnedSignalEmitterListResource, OwnedSignalEmitterResource


class AbstractUserResource(AbstractResource):
    __metaclass__ = ABCMeta

    __custom_error_mappings = {
        'UserAlreadyExistsException': {
            'code': 409,
            'message': lambda e: str(e)
        },
        'SensorAlreadyExistsException': {
            'code': 409,
            'message': lambda e: str(e)
        },
        'SignalEmitterAlreadyExistsException': {
            'code': 409,
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

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings, **kwargs)
        self._user_manager = DependencyContainer.users_manager()
        self._user_serializer = Serializer(UserSchema(strict=True))
        self._sensed_objects_processor = DependencyContainer.sensing_user_object_processor()

    def _do_get_processor(self) -> SensedObjectsProcessor:
        return self._sensed_objects_processor

    def _do_get_owner(self, owner_id: str):
        return self._user_manager.get_user(owner_id)

    def _update_owner(self, owner_id: str, owner):
        self._user_manager.update_user(owner_id, owner)


class UserListResource(AbstractUserResource):
    """
    Resource representing Users in the system
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _do_get(self):
        return self._user_serializer.serialize(self._user_manager.get_all_users())

    def _do_post(self):
        user = self._user_serializer.deserialize(self._get_post_data_as_json())
        return self._user_serializer.serialize(self._user_manager.add_user(user_id=user.id, user=user))


class UserResource(AbstractUserResource):
    """
    Resource related to one user in particular in the system
    """

    def _do_get(self, user_id):
        return self._user_serializer.serialize(self._user_manager.get_user(user_id=user_id))

class SensingUserSensorListResource(AbstractUserResource, OwnedSensorListResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class SensingUserSensorResource(AbstractUserResource, OwnedSensorResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class SignalEmittingUserSEListResource(AbstractUserResource, OwnedSignalEmitterListResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class SignalEmittingUserSEResource(AbstractUserResource, OwnedSignalEmitterResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


