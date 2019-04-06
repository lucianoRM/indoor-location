from typing import List

from src.core.data.sensed_object import SensedObject
from src.core.data.sensed_objects_processor import SensedObjectsProcessor
from src.core.database.kv_database import KeyDoesNotExistException, KVDatabase
from src.core.location.location_service import LocationService
from src.core.manager.kvdb_backed_manager import KVDBBackedManager
from src.core.sensor.sensors_manager import SensorsManager
from src.core.user.users_manager import UsersManager


class KVDBSensedObjectsProcessor(KVDBBackedManager, SensedObjectsProcessor):
    """
    A data processor that backs all information needed in a Key-Value database
    """

    #Key to store which sensors have sensed which objects to be able to compute their location properly. The keys are the objects ids and the values are the sensors that are in range of those objects
    __SENSED_BY_KEY = "objects_sensed_by"

    def __init__(self, database: KVDatabase, sensors_manager: SensorsManager, users_manager: UsersManager, location_service: LocationService):
        super().__init__(database)
        self.__sensor_manager = sensors_manager
        self.__user_manager = users_manager
        self.__location_service = location_service


    def process_new_data(self, sensor_id: str, objects: List[SensedObject]):
        """
        Process all new data sensed by the sensor and updates moving objects location.

        First we need to get the sensor last sensed objects from the sensor manager. That information will be overriden by the new one.
        Then, we need to update the "objects sensed by" information so that the object's being sensed by the sensor are updated.
        For every sensed object, we add the sensor to it's values if it's not already there
        Then, for every object that the sensor sensed last time, but not now, we remove the sensor id from their values

        Lastly, we update all MovingObject's positions.

        :param sensor_id: The id of the sensor that has the new information
        :param objects: The objects being sensed by the sensor
        """
        objects_ids = set(objects.keys())

        sensor = self.__sensor_manager.get_sensor(sensor_id)
        last_sensed_objects_ids = set(sensor.get_sensed_objects().keys())

        #All objects that were sensed last time but not again this time. These should be now considered out of range
        objects_to_clean = last_sensed_objects_ids - objects_ids

        #New objects sensed by this sensor
        objects_to_add = objects_ids - last_sensed_objects_ids

        try:
            objects_sensed_by = self._database.retrieve(self.__SENSED_BY_KEY)
        except KeyDoesNotExistException:
            objects_sensed_by = {}

        #update objects
        for object_id in objects_to_add:
            sensors_in_range = objects_sensed_by.get(object_id, set([]))
            sensors_in_range.add(sensor_id)
        for object_id in objects_to_clean:
            sensors_in_range = objects_sensed_by.get(object_id)
            if sensors_in_range:
                sensors_in_range.remove(sensor_id)

        sensor.update_sensed_objects(objects)
        self.__sensor_manager.update_sensor(sensor_id=sensor_id, sensor=sensor)

        self._database.upsert(self.__SENSED_BY_KEY, objects_sensed_by)



