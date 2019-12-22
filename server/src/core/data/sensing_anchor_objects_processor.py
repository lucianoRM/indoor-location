from typing import List, Dict

from src.core.anchor.anchors_manager import AnchorsManager
from src.core.data.sensed_object import SensedObject
from src.core.data.sensed_objects_processor import SensedObjectsProcessor
from src.core.database.kv_database import KeyDoesNotExistException, KVDatabase
from src.core.emitter.signal_emitters_manager import SignalEmittersManager, UnknownSignalEmitterException
from src.core.location.location_service import LocationServiceException
from src.core.location.location_service_provider import LocationServiceProvider
from src.core.location.reference_point import ReferencePoint
from src.core.manager.kvdb_backed_manager import KVDBBackedManager
from src.core.object.moving_objects_manager import MovingObjectsManager, UnknownMovingObjectException
from src.core.sensor.sensor import Sensor
from src.core.sensor.sensors_manager import SensorsManager


class SensingAnchorObjectsProcessor(KVDBBackedManager, SensedObjectsProcessor):
    """
    A data processor for sensors that are owned by anchors that backs all information needed in a Key-Value database
    """

    # Key to store which sensors have sensed which objects to be able to compute their location properly.
    # The keys are the objects ids and the values are the sensors that are in range of those objects
    __SENSED_BY_KEY = "objects_sensed_by"

    def __init__(self,
                 database: KVDatabase,
                 anchors_manager: AnchorsManager,
                 sensors_manager: SensorsManager,
                 signal_emitters_manager: SignalEmittersManager,
                 moving_objects_manager: MovingObjectsManager,
                 location_service_provider: LocationServiceProvider):
        super().__init__(database)
        self.__anchors_manager = anchors_manager
        self.__sensor_manager = sensors_manager
        self.__signal_emitters_manager = signal_emitters_manager
        self.__moving_objects_manager = moving_objects_manager
        self.__location_service_provider = location_service_provider

    def process_sensed_objects(self, owner_id: str, sensor_id: str, sensed_objects: List[SensedObject], location_service : str = None):
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

        anchor = self.__anchors_manager.get_anchor(owner_id)
        sensor = anchor.get_sensor(sensor_id)

        last_sensed_objects_ids = set(sensor.get_sensed_objects().keys())

        # All objects that were sensed last time but not again this time. These should be now considered out of range
        objects_to_clean = last_sensed_objects_ids - objects_ids

        # New objects sensed by this sensor
        objects_to_add = objects_ids - last_sensed_objects_ids

        try:
            objects_sensed_by = self._database.retrieve(self.__SENSED_BY_KEY)
        except KeyDoesNotExistException:
            objects_sensed_by = {}

        # update objects
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
        anchor.update_sensor(sensor_id, sensor)

        self.__anchors_manager.update_anchor(owner_id, anchor)
        self.__update_sensed_objects_positions(sensed_objects, objects_sensed_by, location_service)
        self._database.upsert(self.__SENSED_BY_KEY, objects_sensed_by)

    def __update_sensed_objects_positions(self, sensed_objects: List[SensedObject], sensed_by: Dict[str, Sensor], location_service: str):
        # for every sensed objects, get all static sensors and compute it's location.
        for sensed_object in sensed_objects:
            sensed_object_id = sensed_object.id
            sensors_in_range = sensed_by.get(sensed_object_id, {})
            reference_points = []
            for sensor_id in sensors_in_range:
                sensor_owner = self.__sensor_manager.get_owner(sensor_id)
                sensor = sensor_owner.get_sensor(sensor_id)
                sensor_position = sensor_owner.position
                sensed_moving_object = sensor.get_sensed_objects().get(sensed_object_id)
                reference_points.append(ReferencePoint(
                    position=sensor_position,
                    distance=sensed_moving_object.data.distance,
                    timestamp=sensed_moving_object.data.timestamp
                ))
            try:
                signal_emitter_owner = self.__signal_emitters_manager.get_owner(sensed_object_id)
                signal_emitter_owner.position = self.__location_service_provider.get_location_service(location_service).locate_object(reference_points=reference_points)
                self.__moving_objects_manager.update_moving_object(object_id=signal_emitter_owner.id, object=signal_emitter_owner)
            except (UnknownSignalEmitterException, UnknownMovingObjectException):
                # TODO: Check what to do in these situations
                continue
            except LocationServiceException:
                pass
