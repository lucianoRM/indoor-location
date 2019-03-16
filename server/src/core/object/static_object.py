from src.core.object.positionable_object import PositionableObject


class StaticObject(PositionableObject):
    """
    Class to model a PositionableObject that does not modify it's position in the system
    """

    def __init__(self, id, position, **kwargs):
        super(StaticObject, self).__init__(id, position, **kwargs)

    def doSomething(self):
        print "hola"