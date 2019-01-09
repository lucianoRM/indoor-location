import unittest

from src.core.exception.exceptions import IllegalArgumentException
from src.core.user.user import User


class UserTestCase(unittest.TestCase):

    def test_create_user_and_get_values(self):
        name = 'luciano'
        id = 'theId'
        location = (5,5)
        user = User(**{User.NAME_KEY:name, User.ID_KEY:id, User.LOCATION_KEY:location})
        self.assertEquals(user.name, name)
        self.assertEquals(user.id, id)
        self.assertEquals(user.location, location)

    def test_default_values(self):
        user = User(**{User.NAME_KEY:'name'})
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.location)

    def test_user_fails_if_missing_argument(self):
        self.assertRaises(IllegalArgumentException, User)