from src.core.exception.exceptions import IllegalArgumentException


class User:
    """
    Stores all information related to an User using the system
    """

    NAME_KEY = "name"
    ID_KEY = "id"
    LOCATION_KEY = "location"

    def __init__(self, **kwargs):
        """
        Constructor for User. It receives keyworded arguments to simulate a builder pattern.
        Only mandatory parameters will be validated. Otherwise, a default value will be used.
        :raises IllegalArgumentException: If mandatory arguments are not present
        :param kwargs: arguments to build the user
        """
        self.name = kwargs.get(self.NAME_KEY)
        self.id = kwargs.get(self.ID_KEY)
        self.location = kwargs.get(self.LOCATION_KEY, self.__generate_starting_location())
        if not self.name:
            raise IllegalArgumentException("User must define a name")
        if not self.id:
            raise IllegalArgumentException("User must define an id")

    def __generate_starting_location(self):
        return (0,0)