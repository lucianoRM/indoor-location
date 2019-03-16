from src.core.object.positionable_object import PositionableObject


class MovingObject(PositionableObject):
    """
    Class to modelate an object that changes it's position in the system
    """

    @PositionableObject.position.setter
    def position(self, position):
        self._position = position