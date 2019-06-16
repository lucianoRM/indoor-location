
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.user_schema import UserSchema

class UserListResource(AbstractResource):
    '''
    Resource representing Users in the system
    '''

    __custom_error_mappings = {
        'UserAlreadyExistsException': {
            'code': 409,
            'message': lambda e: str(e)
        }
    }

    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings, **kwargs)
        self.__user_manager = DependencyContainer.users_manager()
        self.__users_schema = UserSchema(many=True, strict=True)
        self.__user_schema = UserSchema(strict=True)

    def _do_get(self):
        return self.__users_schema.dump(self.__user_manager.get_all_users())

    def _do_post(self):
        user = self.__user_schema.load(self._get_post_data_as_json()).data
        return self.__user_schema.dump(self.__user_manager.add_user(user_id=user.id, user=user))


class UserResource(AbstractResource):
    '''
    Resource related to one user in particular in the system
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__user_manager = DependencyContainer.users_manager()
        self.__user_schema = UserSchema(strict=True)

    def _do_get(self, user_id):
        return self.__user_schema.dump(self.__user_manager.get_user(user_id=user_id))



