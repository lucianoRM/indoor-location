from typing import List

from src.core.data.sensed_object import SensedObject
from src.core.data.sensed_objects_processor import SensedObjectsProcessor
from src.core.emitter.signal_emitters_manager import SignalEmittersManager
from src.core.location.location_service import LocationService
from src.core.location.simple_location_service import Anchor
from src.core.object.moving_object import MovingObject
from src.core.object.static_objects_manager import UnknownStaticObjectException
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
                 location_service: LocationService):
        super().__init__()
        self.__sensor_manager = sensors_manager
        self.__users_manager = users_manager
        self.__signal_emitters_manager = signal_emitters_manager
        self.__location_service = location_service

    def process_sensed_objects(self, owner_id: str, sensor_id: str, sensed_objects: List[SensedObject]):

        user = self.__users_manager.get_user(owner_id)
        sensor = user.sensors.get(sensor_id)
        sensor.update_sensed_objects(sensed_objects)
        user.update_sensor(sensor_id, sensor)

        self.__update_owner_position(user, sensed_objects)

        self.__users_manager.update_user(owner_id, user)

    def __update_owner_position(self, owner: MovingObject, sensed_objects: List[SensedObject]):
        anchor_objects = []
        for sensed_object in sensed_objects:
            id = sensed_object.id
            try:
                anchor_objects.append(
                    Anchor(position=self.__signal_emitters_manager.locate_signal_emitter(signal_emitter_id=id),
                           distance=sensed_object.data.distance,
                           timestamp=sensed_object.data.timestamp))
            except UnknownStaticObjectException:
                # TODO: Check what to do in these cases, when id's can't be found
                continue
        new_position = self.__location_service.locate_object(anchor_objects)
        owner.position = new_position
