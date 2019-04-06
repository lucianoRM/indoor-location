from abc import ABCMeta, abstractmethod
from typing import List

from src.core.data.sensed_object import SensedObject


class SensedObjectsProcessor:
    """
    Handles all new sensed data entering the system and process it so that it can later be correctly queried.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def process_new_data(self, sensor_id: str, objects: List[SensedObject]):
        """Processes new sensed objects from sensor with sensor_id"""
        raise NotImplementedError