from src.core.exception.exceptions import IllegalArgumentException

NAME_KEY = "name"
ID_KEY = "id"
POSITION_KEY = "position"

class User:
    """
    Stores all information related to an User using the system
    """

    def __init__(self, **kwargs):
        """
        Constructor for User. It receives keyworded arguments to simulate a builder pattern.
        Only mandatory parameters will be validated. Otherwise, a default value will be used.
        :raises IllegalArgumentException: If mandatory arguments are not present
        :param kwargs: arguments to build the user
        """
        self.name = kwargs.get(NAME_KEY)
        self.id = kwargs.get(ID_KEY)
        self.position = kwargs.get(POSITION_KEY, self.__generate_starting_position())
        if not self.name:
            raise IllegalArgumentException("User must define a name")
        if not self.id:
            raise IllegalArgumentException("User must define an id")

    def __generate_starting_position(self):
        return (0,0)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id and self.name == other.name and self.position == other.position
        return False

    def __ne__(self, other):
        return not self.__eq__(other)