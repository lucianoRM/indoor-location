from src.core.exception.exceptions import IllegalArgumentException

NAME_KEY = "name"
ID_KEY = "id"
LOCATION_KEY = "location"

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
        self.location = kwargs.get(LOCATION_KEY, self.__generate_starting_location())
        if not self.name:
            raise IllegalArgumentException("User must define a name")
        if not self.id:
            raise IllegalArgumentException("User must define an id")

    def __generate_starting_location(self):
        return (0,0)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id and self.name == other.name and self.location == other.location
        return False

    def __ne__(self, other):
        return not self.__eq__(other)