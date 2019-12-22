from copy import deepcopy
from typing import Dict, List

from src.core.data.sensed_object import SensedObject
from src.core.object.moving_object import MovingObject

class Sensor(MovingObject):
    """
    Class to simulate a signal sensor
    Stores all information related to a sensor that is part of the system.
    Keep in mind that sensors can be any kind of device that senses data. If it contributes new data to the system,
    it should be a Sensor.
    """

    def __init__(self, **kwargs):
        #Dict to store the objects that where located by this sensor. It should have the objects id as key and the sensed data as value
        self.__sensed_objects = {}
        super().__init__(**kwargs)

    def update_sensed_objects(self, sensed_objects: List[SensedObject], merge=False):
        """
        Updates stored sensed data with the new one
        :param sensed_objects: The new sensed data corresponding to this sensor
        :param merge: True if the new data should be merged with the old, overriding values with same key. False if all old sensed data should be replaced with new.
        """
        sensed_objects_dict = {}
        for sensed_object in sensed_objects:
            sensed_objects_dict[sensed_object.id] = sensed_object
        if(merge):
            for (key,value) in sensed_objects_dict.items() : self.__sensed_objects[key] = value
        else:
            self.__sensed_objects = sensed_objects_dict

    def get_sensed_objects(self) -> Dict[str, SensedObject]:
        return deepcopy(self.__sensed_objects)