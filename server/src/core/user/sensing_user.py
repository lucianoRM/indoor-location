from src.core.sensor.sensor import Sensor
from src.core.user.user import User


class SensingUser(User, Sensor):
    """
    An user that is also a sensor.
    """

    def __init__(self, id, position, **kwargs):
        super().__init__(id=id, position=position, **kwargs)



