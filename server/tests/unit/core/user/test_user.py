from unittest import TestCase

from src.core.exception.exceptions import IllegalArgumentException
from src.core.user.user import User, LOCATION_KEY, ID_KEY, NAME_KEY


class UserTestCase(TestCase):

    def test_create_user_and_get_values(self):
        name = 'luciano'
        id = 'theId'
        location = (5,5)
        user = User(**{NAME_KEY:name, ID_KEY:id, LOCATION_KEY:location})
        self.assertEquals(user.name, name)
        self.assertEquals(user.id, id)
        self.assertEquals(user.location, location)

    def test_default_values(self):
        user = User(**{NAME_KEY:'name', ID_KEY : "userId"})
        self.assertIsNotNone(user.location)

    def test_user_fails_if_missing_argument(self):
        self.assertRaises(IllegalArgumentException, User)