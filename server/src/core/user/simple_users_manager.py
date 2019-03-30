from src.core.database.kv_database import KeyAlreadyExistsException, KeyDoesNotExistException
from src.core.manager.kvdb_backed_manager import KVDBBackedManager
from src.core.object.moving_objects_manager import MovingObjectAlreadyExistsException, UnknownMovingObjectException
from src.core.user.user_manager import UsersManager, UserAlreadyExistsException, UnknownUserException


class SimpleUsersManager(UsersManager):
    """User manager that stores information in a key-value database"""

    def __init__(self, moving_objects_manager):
        """
        Constructor for Manager.
        :param moving_objects_manager: manager for moving objects where users will be stored
        """
        self.__moving_objects_manager = moving_objects_manager

    def add_user(self, user_id, user):
        try:
            return self.__moving_objects_manager.add_moving_object(object_id=user_id, object=user)
        except MovingObjectAlreadyExistsException:
            raise UserAlreadyExistsException("User with id: " + user_id + " was already registered")

    def get_user(self, user_id):
        try:
            return self.__moving_objects_manager.get_moving_object(object_id=user_id)
        except UnknownMovingObjectException:
            raise UnknownUserException("An user with id: " + user_id + " does not exist")

    def update_user(self, user_id, user):
        try:
            return self.__moving_objects_manager.update_moving_object(object_id=user_id, object=user)
        except UnknownMovingObjectException:
            raise UnknownUserException("An user with id: " + user_id + " does not exist")

    def remove_user(self, user_id):
        try:
            return self.__moving_objects_manager.remove_moving_object(object_id=user_id)
        except KeyDoesNotExistException:
            raise UnknownUserException("Attempting to remove an user that does not exist. With ID: " + user_id)

    def get_all_users(self):
        try:
            return self.__moving_objects_manager.get_all_moving_objects()
        except KeyDoesNotExistException:
            return []

