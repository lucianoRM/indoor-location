from src.core.database.kv_database import KeyAlreadyExistsException, KeyDoesNotExistException
from src.core.manager.kvdb_backed_manager import KVDBBackedManager
from src.core.user.user_manager import UserManager, UserAlreadyExistsException, UnknownUserException


class KVDBUserManager(UserManager, KVDBBackedManager):
    """User manager that stores information in a key-value database"""

    __USERS_LOCATION_KEY = "users"

    def __init__(self, kv_database):
        """
        Constructor for Manager.
        :param kv_database: key-value database to store information about users
        """
        super(KVDBUserManager, self).__init__(kv_database)

    def add_user(self, user):
        try:
            return self._database.insert(
                self._build_complex_key(self.__USERS_LOCATION_KEY, user.id),
                user
            )
        except KeyAlreadyExistsException:
            raise UserAlreadyExistsException("User with id: " + user.id + " was already registered")

    def get_user(self, userId):
        try:
            return self._database.retrieve(
                self._build_complex_key(self.__USERS_LOCATION_KEY, userId)
            )
        except KeyDoesNotExistException:
            raise UnknownUserException("An user with id: " + userId + " does not exist")

    def update_user(self, userId, user):
        try:
            return self._database.update(
                self._build_complex_key(self.__USERS_LOCATION_KEY, userId),
                user
            )
        except KeyDoesNotExistException:
            raise UnknownUserException("An user with id: " + userId + " does not exist")

    def remove_user(self, userId):
        try:
            return self._database.remove(
                self._build_complex_key(self.__USERS_LOCATION_KEY, userId)
            )
        except KeyDoesNotExistException:
            raise UnknownUserException("Attempting to remove an user that does not exist. With ID: " + userId)

    def get_all_users(self):
        try:
            return self._database.retrieve(self.__USERS_LOCATION_KEY).values()
        except KeyDoesNotExistException:
            return []

