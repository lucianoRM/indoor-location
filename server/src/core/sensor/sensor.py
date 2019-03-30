from abc import ABCMeta, abstractmethod
from copy import deepcopy

class Sensor:
    """
    Abstract class to simulate a signal sensor
    Stores all information related to a sensor that is part of the system.
    Keep in mind that sensors can be any kind of device that senses data. If it contributes new data to the system,
    it should be a Sensor.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        #Dict to store the objects that where located by this sensor. It should have the objects id as key and the sensed data as value
        self.__sensed_objects = {}

    def update_sensed_objects(self, sensed_objects, merge=False):
        """
        Updates stored sensed data with the new one
        :param sensed_objects: The new sensed data corresponding to this sensor
        :param merge: True if the new data should be merged with the old, overriding values with same key. False if all old sensed data should be replaced with new.
        """
        if(merge):
            for (key,value) in sensed_objects.items() : self.__sensed_objects[key] = value
        else:
            self.__sensed_objects = sensed_objects

    def get_sensed_objects(self):
        return deepcopy(self.__sensed_objects)