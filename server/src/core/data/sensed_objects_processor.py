from abc import ABCMeta, abstractmethod


class SensedObjectsProcessor(object):
    """
    Handles all new sensed data entering the system and process it so that it can later be correctly queried.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def process_new_data(self, sensor_id, objects):
        """Processes new sensed objects from sensor with sensor_id"""
        raise NotImplementedError