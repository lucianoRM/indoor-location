from unittest import TestCase

from src.core.exception.exceptions import IllegalArgumentException
from src.core.user.user import User, POSITION_KEY, ID_KEY, NAME_KEY


class UserTestCase(TestCase):

    def test_create_user_and_get_values(self):
        name = 'luciano'
        id = 'theId'
        position = (5,5)
        user = User(name=name, id=id, position=position)
        self.assertEquals(user.name, name)
        self.assertEquals(user.id, id)
        self.assertEquals(user.position, position)