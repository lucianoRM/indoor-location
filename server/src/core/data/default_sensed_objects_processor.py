from abc import ABCMeta, abstractmethod
from typing import List, Dict

from src.core.data.sensed_object import SensedObject
from src.core.data.sensed_objects_processor import SensedObjectsProcessor
from src.core.database.kv_database import KeyDoesNotExistException, KVDatabase
from src.core.location.location_service import LocationService, LocationServiceException
from src.core.location.simple_location_service import Anchor
from src.core.manager.kvdb_backed_manager import KVDBBackedManager
from src.core.object.moving_object import MovingObject
from src.core.object.moving_objects_manager import MovingObjectsManager, UnknownMovingObjectException
from src.core.object.static_object import StaticObject
from src.core.object.static_objects_manager import StaticObjectsManager, UnknownStaticObjectException
from src.core.sensor.sensor import Sensor
from src.core.sensor.sensors_manager import SensorsManager, UnknownSensorException


class DefaultSensedObjectsProcessor(KVDBBackedManager, SensedObjectsProcessor):
    """
    A data processor that backs all information needed in a Key-Value database
    """

    #Key to store which sensors have sensed which objects to be able to compute their location properly. The keys are the objects ids and the values are the sensors that are in range of those objects
    __SENSED_BY_KEY = "objects_sensed_by"

    def __init__(self,
                 database: KVDatabase,
                 sensors_manager: SensorsManager,
                 static_objects_manager: StaticObjectsManager,
                 moving_objects_manager: MovingObjectsManager,
                 location_service: LocationService):
        super().__init__(database)
        self.__sensor_manager = sensors_manager
        self.__static_objects_manager = static_objects_manager
        self.__moving_objects_manager = moving_objects_manager
        self.__location_service = location_service

    def process_sensed_objects(self, sensor_id: str, sensed_objects : List[SensedObject]):
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
        objects_ids = set([object.id for object in sensed_objects])

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
            objects_sensed_by[object_id] = sensors_in_range
        for object_id in objects_to_clean:
            sensors_in_range = objects_sensed_by.get(object_id)
            if sensors_in_range:
                sensors_in_range.remove(sensor_id)
            objects_sensed_by[object_id] = sensors_in_range

        sensor.update_sensed_objects(sensed_objects)
        self.__sensor_manager.update_sensor(sensor_id=sensor_id, sensor=sensor)

        if isinstance(sensor, MovingObject):
            self.__update_sensor_position(sensor, sensed_objects)
        elif isinstance(sensor, StaticObject):
            self.__update_sensed_objects_positions(sensed_objects, objects_sensed_by)

        self._database.upsert(self.__SENSED_BY_KEY, objects_sensed_by)


    def __update_sensor_position(self, sensor: MovingObject, sensed_objects: List[SensedObject]):
        anchor_objects = []
        for sensed_object in sensed_objects:
            id = sensed_object.id
            try:
                retrieved_object = self.__static_objects_manager.get_static_object(object_id=id)
                anchor_objects.append(Anchor(position=retrieved_object.position, distance=sensed_object.data.distance,
                                             timestamp=sensed_object.data.timestamp))
            except UnknownStaticObjectException:
                #TODO: Check what to do in these cases, when id's can't be found
                continue
        new_position = self.__location_service.locate_object(anchor_objects)
        sensor.position = new_position
        self.__sensor_manager.update_sensor(sensor_id=sensor.id, sensor=sensor)

    def __update_sensed_objects_positions(self, sensed_objects : List[SensedObject], sensed_by : Dict[str, Sensor]):
        #for every sensed objects, get all static sensors and compute it's location.
        for sensed_object in sensed_objects:
            sensed_object_id = sensed_object.id
            sensors_in_range = sensed_by.get(sensed_object_id, {})
            anchors = []
            for sensor_id in sensors_in_range:
                sensor = self.__sensor_manager.get_sensor(sensor_id=sensor_id)
                sensed_moving_object = sensor.get_sensed_objects().get(sensed_object_id)
                anchors.append(Anchor(
                    position=sensor.position,
                    distance=sensed_moving_object.data.distance,
                    timestamp=sensed_moving_object.data.timestamp
                ))
            try:
                moving_object = self.__moving_objects_manager.get_moving_object(object_id=sensed_object_id)
                moving_object.position = self.__location_service.locate_object(anchors=anchors)
                self.__moving_objects_manager.update_moving_object(object_id=sensed_object_id, object=moving_object)
            except UnknownMovingObjectException:
                #TODO: Check what to do in these situations
                continue
            except LocationServiceException:
                pass


