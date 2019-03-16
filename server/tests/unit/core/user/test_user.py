from unittest import TestCase

from src.core.exception.exceptions import IllegalArgumentException
from src.core.user.user import User, POSITION_KEY, ID_KEY, NAME_KEY


class UserTestCase(TestCase):

    def test_create_user_and_get_values(self):
        name = 'luciano'
        id = 'theId'
        position = (5,5)
        user = User(**{NAME_KEY:name, ID_KEY:id, POSITION_KEY:position})
        self.assertEquals(user.name, name)
        self.assertEquals(user.id, id)
        self.assertEquals(user.position, position)

    def test_default_values(self):
        user = User(**{NAME_KEY:'name', ID_KEY : "userId"})
        self.assertIsNotNone(user.position)

    def test_user_fails_if_missing_argument(self):
        self.assertRaises(IllegalArgumentException, User)