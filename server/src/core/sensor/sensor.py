from abc import ABCMeta
from copy import deepcopy

from src.core.object.positionable_object import PositionableObject


class Sensor(PositionableObject):
    """
    Stores all information related to a sensor that is part of the system.
    Keep in mind that sensors can be any kind of device that senses data. If it contributes new data to the system,
    it should be a Sensor.
    """

    def __init__(self, id, position, **kwargs):
        super(Sensor, self).__init__(id, position, **kwargs)

        #Dict to store the objects that where located by this sensor. It should have the objects id as key and the sensed data as value
        self.__sensed_objects = {}

    def update_sensed_objects(self, sensed_data, merge=False):
        """
        Updates stored sensed data with the new one
        :param sensed_data: The new sensed data corresponding to this sensor
        :param merge: True if the new data should be merged with the old, overriding values with same key. False if all old sensed data should be replaced with new.
        """
        if(merge):
            for (key,value) in sensed_data.items() : self.__sensed_objects[key] = value
        else:
            self.__sensed_objects = sensed_data

    def get_sensed_objects(self):
        return deepcopy(self.__sensed_objects)