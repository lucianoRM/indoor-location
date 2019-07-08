from abc import ABCMeta, abstractmethod

from src.core.data.sensed_objects_processor import SensedObjectsProcessor
from src.core.object.sensor_aware_object import SensorAwareObject
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.serializer import Serializer
from src.resources.schemas.user_schema import UserSchema
from src.resources.sensors_resources import OwnedSensorListResource, OwnedSensorResource


class AbstractUserResource(AbstractResource):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._user_manager = DependencyContainer.users_manager()
        self._serializer = Serializer(UserSchema(strict=True))


class UserListResource(AbstractUserResource):
    """
    Resource representing Users in the system
    """

    __custom_error_mappings = {
        'UserAlreadyExistsException': {
            'code': 409,
            'message': lambda e: str(e)
        },
        'SensorAlreadyExistsException': {
            'code': 400,
            'message': lambda e: str(e)
        },
        'SignalEmitterAlreadyExistsException': {
            'code': 400,
            'message': lambda e: str(e)
        }
    }

    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings, **kwargs)

    def _do_get(self):
        return self._serializer.serialize(self._user_manager.get_all_users())

    def _do_post(self):
        user = self._serializer.deserialize(self._get_post_data_as_json())
        return self._serializer.serialize(self._user_manager.add_user(user_id=user.id, user=user))


class UserResource(AbstractUserResource):
    """
    Resource related to one user in particular in the system
    """

    def _do_get(self, user_id):
        return self._serializer.serialize(self._user_manager.get_user(user_id=user_id))


class AbstractSensingUserResource(AbstractUserResource):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__sensed_objects_processor = DependencyContainer.sensing_user_object_processor()

    def _do_get_processor(self) -> SensedObjectsProcessor:
        return self.__sensed_objects_processor


class SensingUserSensorListResource(AbstractSensingUserResource, OwnedSensorListResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SensingUserSensorResource(AbstractSensingUserResource, OwnedSensorResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
