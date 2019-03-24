from src.core.data.sensed_objects_processor import SensedObjectsProcessor
from src.core.database.kv_database import KeyDoesNotExistException
from src.core.manager.kvdb_backed_manager import KVDBBacked


class KVDBSensedObjectsProcessor(KVDBBacked, SensedObjectsProcessor):
    """
    A data processor that backs all information needed in a Key-Value database
    """

    #Key to store which sensors have sensed which objects to be able to compute their location properly
    __SENSED_OBJECTS_KEY = "sensed_objects"

    def __init__(self, database, sensor_manager, user_manager, location_service):
        super(KVDBSensedObjectsProcessor, self).__init__(database)
        self.__sensor_manager = sensor_manager
        self.__user_manager = user_manager
        self.__location_service = location_service


    def process_new_data(self, sensor_id, objects):
        objects_ids = set(objects.keys())

        sensor = self.__sensor_manager.get_sensor(sensor_id)
        last_sensed_objects_ids = set(sensor.get_sensed_objects().keys())

        #All objects that were sensed last time but not again this time. These should be now considered out of range
        objects_to_clean = last_sensed_objects_ids - objects_ids

        #New objects sensed by this sensor
        objects_to_add = objects_ids - last_sensed_objects_ids

        try:
            sensed_objects_information = self._database.retrieve(self.__SENSED_OBJECTS_KEY)
        except KeyDoesNotExistException:
            sensed_objects_information = {}

        #update objects
        for object_id in objects_to_add:
            sensors_in_range = sensed_objects_information.get(object_id, set([]))
            sensors_in_range.add(sensor_id)
        for object_id in objects_to_clean:
            sensors_in_range = sensed_objects_information.get(object_id)
            if sensors_in_range:
                sensors_in_range.remove(sensor_id)

        sensor.update_sensed_objects(objects)
        self.__sensor_manager.update_sensor(sensorId=sensor_id, sensor=sensor)

        self._database.upsert(self.__SENSED_OBJECTS_KEY, sensed_objects_information)



