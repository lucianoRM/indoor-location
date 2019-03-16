from unittest import TestCase

from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.user.user import User, ID_KEY, NAME_KEY, POSITION_KEY
from src.core.user.kvdb_user_manager import KVDBUserManager
from src.core.user.user_manager import UserAlreadyExistsException, UnknownUserException


class KVDBUserManagerTestCase(TestCase):

    __USER_ID = "userId"

    def setUp(self):
        self.__test_user = User(**{ID_KEY : self.__USER_ID,
                                     NAME_KEY : "userName",
                                     POSITION_KEY : (0,0)})
        self.__user_manager = KVDBUserManager(MemoryKVDatabase())

    def test_add_user(self):
        self.__user_manager.add_user(self.__test_user)
        self.assertEquals(self.__user_manager.get_user(self.__USER_ID), self.__test_user)

    def test_add_user_with_same_id(self):
        self.__user_manager.add_user(self.__test_user)
        sameIdUser = User(**{ID_KEY : self.__USER_ID,
                                     NAME_KEY : "otherUser",
                                     POSITION_KEY : (1,1)})
        self.assertRaises(UserAlreadyExistsException,self.__user_manager.add_user, sameIdUser)

    def test_add_multiple_users_and_get_all(self):
        all_users = [User(**{ID_KEY:str(userId), NAME_KEY:"userName", POSITION_KEY: (0,0)}) for userId in xrange(100)]
        for user in all_users:
            self.__user_manager.add_user(user)
        retrieved_users = self.__user_manager.get_all_users()
        for user in all_users:
            self.assertTrue(user in retrieved_users)

    def test_remove_user_and_try_get_it(self):
        self.__user_manager.add_user(self.__test_user)
        self.assertEquals(self.__user_manager.get_user(self.__USER_ID), self.__test_user)
        self.__user_manager.remove_user(self.__USER_ID)
        self.assertRaises(UnknownUserException, self.__user_manager.get_user, self.__USER_ID)

    def test_get_user_from_empty_db(self):
        self.assertRaises(UnknownUserException,self.__user_manager.get_user, self.__USER_ID)

    def test_update_user(self):
        self.__user_manager.add_user(self.__test_user)
        newUser = User(**{ID_KEY: self.__USER_ID,
                          NAME_KEY: "newUserName",
                          POSITION_KEY: (1, 1)})
        self.__user_manager.update_user(self.__USER_ID,
                                            newUser)
        self.assertEquals(self.__user_manager.get_user(self.__USER_ID), newUser)

    def test_update_not_existent_user(self):
        self.assertRaises(UnknownUserException, self.__user_manager.update_user, "missingUserId", {})