from pytest import fixture, raises

from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.object.kvdb_moving_objects_manager import KVDBMovingObjectsManager
from src.core.user.default_users_manager import DefaultUsersManager
from src.core.user.users_manager import UserAlreadyExistsException, UnknownUserException
from tests.unit.test_implementations.implementations import TestUser


class TestDefaultUsersManager:

    __USER_ID = "user_id"

    @fixture(autouse=True)
    def setUp(self):
        self.__test_user = TestUser(id=self.__USER_ID,
                                name="userName",
                                position=(0,0))
        self.__user_manager = DefaultUsersManager(KVDBMovingObjectsManager(MemoryKVDatabase()))

    def test_add_user(self):
        self.__user_manager.add_user(user_id=self.__USER_ID, user=self.__test_user)
        assert self.__user_manager.get_user(self.__USER_ID) == self.__test_user

    def test_add_user_with_same_id(self):
        self.__user_manager.add_user(user_id=self.__USER_ID, user=self.__test_user)
        sameIdUser = TestUser(id=self.__USER_ID,
                                name="otherUser",
                                position=(1,1))
        with raises(UserAlreadyExistsException):
            self.__user_manager.add_user(user_id=self.__USER_ID, user=sameIdUser)

    def test_add_multiple_users_and_get_all(self):
        all_users = [TestUser(id=str(userId), name="userName", position=(0,0)) for userId in range(100)]
        for user in all_users:
            self.__user_manager.add_user(user_id=user.id, user=user)
        retrieved_users = self.__user_manager.get_all_users()
        for user in all_users:
            assert user in retrieved_users

    def test_remove_user_and_try_get_it(self):
        self.__user_manager.add_user(user_id=self.__USER_ID, user=self.__test_user)
        assert self.__user_manager.get_user(self.__USER_ID) == self.__test_user
        self.__user_manager.remove_user(self.__USER_ID)
        with raises(UnknownUserException):
            self.__user_manager.get_user(user_id=self.__USER_ID)

    def test_get_user_from_empty_db(self):
        with raises(UnknownUserException):
            self.__user_manager.get_user(user_id=self.__USER_ID)

    def test_update_user(self):
        self.__user_manager.add_user(user_id=self.__USER_ID, user=self.__test_user)
        newUser = TestUser(id=self.__USER_ID,
                                name="newUserName",
                                position=(1,1))
        self.__user_manager.update_user(self.__USER_ID,
                                            newUser)
        assert self.__user_manager.get_user(user_id=self.__USER_ID) == newUser

    def test_update_not_existent_user(self):
        with raises(UnknownUserException):
            self.__user_manager.update_user(user_id="missingUserId", user={})