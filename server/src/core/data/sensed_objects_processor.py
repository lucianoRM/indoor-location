from abc import ABCMeta, abstractmethod
from typing import List

from src.core.data.sensed_object import SensedObject


class SensedObjectsProcessor:
    """
    Process sensed objects and updates information in the system related to those sensed objects
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def process_sensed_objects(self, sensor_id: str, sensed_objects : List[SensedObject]):
        """Processes new sensed information from sensor with sensor_id"""
        raise NotImplementedError