
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from src.core.anchor.default_anchors_manager import DefaultAnchorsManager
from src.core.data.sensing_anchor_objects_processor import SensingAnchorObjectsProcessor
from src.core.data.sensing_user_objects_processor import SensingUserObjectsProcessor
from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.emitter.default_signal_emitters_manager import DefaultSignalEmittersManager
from src.core.location.geometric_location_service import GeometricLocationService
from src.core.location.location_service_provider import LocationServiceProvider
from src.core.location.oa_location_service import OALocationService
from src.core.location.simple_location_service import SimpleLocationService
from src.core.log.server_logger_factory import get_server_logger
from src.core.manager.default_positionable_objects_manager import PositionableObjectsManagerObserver
from src.core.object.kvdb_moving_objects_manager import KVDBMovingObjectsManager
from src.core.object.kvdb_static_objects_manager import KVDBStaticObjectsManager
from src.core.sensor.default_sensors_manager import DefaultSensorsManager
from src.core.user.default_users_manager import DefaultUsersManager
from src.resources.schemas.anchor_schema import AnchorSchema
from src.resources.schemas.sensor_schema import SensorSchema
from src.resources.schemas.signal_emitter_schema import SignalEmitterSchema
from src.resources.schemas.user_schema import UserSchema

"""
This is where we can store the dependencies needed to inject into the resources in order to properly work.

Each dependency needs to have a key for the resource to be able to find them
"""


class DependencyContainer(DeclarativeContainer):
    __database = Singleton(MemoryKVDatabase)

    __static_objects_manager = Singleton(KVDBStaticObjectsManager, kv_database=__database)
    __moving_objects_manager = Singleton(KVDBMovingObjectsManager, kv_database=__database)

    # this needs to be a factory because of the way it handles caches. It should have a different cache for every manager
    __objects_manager = Factory(PositionableObjectsManagerObserver,
                                observable_static_objects_manager=__static_objects_manager,
                                observable_moving_objects_manager=__moving_objects_manager)

    logger = Singleton(get_server_logger)

    users_manager = Singleton(DefaultUsersManager, moving_objects_manager=__moving_objects_manager)
    anchors_manager = Singleton(DefaultAnchorsManager, static_objects_manager=__static_objects_manager)

    sensors_manager = Singleton(DefaultSensorsManager, objects_manager=__objects_manager)
    signal_emitters_manager = Singleton(DefaultSignalEmittersManager, objects_manager=__objects_manager)

    user_schema = Singleton(UserSchema)
    sensor_schema = Singleton(SensorSchema)
    anchor_schema = Singleton(AnchorSchema)
    signal_emitter_schema = Singleton(SignalEmitterSchema)

    __simple_location_service = Singleton(SimpleLocationService, logger=logger)
    __geometric_location_service = Singleton(GeometricLocationService, logger=logger)
    __optimized_location_service = Singleton(OALocationService, logger=logger)

    location_service_provider = Singleton(LocationServiceProvider,
                                          simple=__simple_location_service,
                                          geometric=__geometric_location_service,
                                          optimized=__optimized_location_service)

    sensing_user_object_processor = Singleton(SensingUserObjectsProcessor,
                                              sensors_manager=sensors_manager,
                                              users_manager=users_manager,
                                              signal_emitters_manager=signal_emitters_manager,
                                              location_service_provider=location_service_provider)

    sensing_anchor_object_processor = Singleton(SensingAnchorObjectsProcessor,
                                                database=__database,
                                                anchors_manager=anchors_manager,
                                                sensors_manager=sensors_manager,
                                                signal_emitters_manager=signal_emitters_manager,
                                                moving_objects_manager=__moving_objects_manager,
                                                location_service_provider=location_service_provider)

    @classmethod
    def reset_singletons(cls):
        for provider in cls.providers.values():
            if isinstance(provider, Singleton):
                provider.reset()

    @classmethod
    def init(cls):
        for provider in cls.providers.values():
            if isinstance(provider, Singleton):
                provider()
