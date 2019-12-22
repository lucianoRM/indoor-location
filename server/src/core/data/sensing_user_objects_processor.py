from typing import List

from src.core.data.sensed_object import SensedObject
from src.core.data.sensed_objects_processor import SensedObjectsProcessor
from src.core.emitter.signal_emitters_manager import SignalEmittersManager, UnknownSignalEmitterException
from src.core.location.location_service_provider import LocationServiceProvider
from src.core.location.reference_point import ReferencePoint
from src.core.object.moving_object import MovingObject
from src.core.sensor.sensors_manager import SensorsManager
from src.core.user.users_manager import UsersManager


class SensingUserObjectsProcessor(SensedObjectsProcessor):
    """
    A data processor for sensors owned by users
    """

    def __init__(self,
                 sensors_manager: SensorsManager,
                 users_manager: UsersManager,
                 signal_emitters_manager: SignalEmittersManager,
                 location_service_provider: LocationServiceProvider):
        super().__init__()
        self.__sensor_manager = sensors_manager
        self.__users_manager = users_manager
        self.__signal_emitters_manager = signal_emitters_manager
        self.__location_service_provider = location_service_provider

    def process_sensed_objects(self, owner_id: str, sensor_id: str, sensed_objects: List[SensedObject], location_service: str = None):

        user = self.__users_manager.get_user(owner_id)
        sensor = user.get_sensor(sensor_id)
        sensor.update_sensed_objects(sensed_objects)
        user.update_sensor(sensor_id, sensor)

        self.__update_owner_position(user, sensed_objects, location_service)

        self.__users_manager.update_user(owner_id, user)

    def __update_owner_position(self, owner: MovingObject, sensed_objects: List[SensedObject], location_service: str):
        anchor_objects = []
        for sensed_object in sensed_objects:
            id = sensed_object.id
            try:
                signal_emitter_owner = self.__signal_emitters_manager.get_owner(id)
                anchor_objects.append(
                    ReferencePoint(position=signal_emitter_owner.position,
                           distance=sensed_object.data.distance,
                           timestamp=sensed_object.data.timestamp))
                #TODO: FOR DEBUGGING, REMOVE
                sensed_debug_info = owner.attributes.get('sensed', {})
                sensed_debug_info.update({id:{'position':signal_emitter_owner.position, 'distance':sensed_object.data.distance}})
                owner.attributes['sensed'] = sensed_debug_info
            except UnknownSignalEmitterException:
                # TODO: Check what to do in these cases, when id's can't be found
                continue
        new_position = self.__location_service_provider.get_location_service(location_service).locate_object(anchor_objects)
        owner.position = new_position
