from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from src.core.anchor.default_anchors_manager import DefaultAnchorsManager
from src.core.data.kvdb_sensed_objects_processor import KVDBSensedObjectsProcessor
from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.emitter.default_signal_emitters_manager import DefaultSignalEmittersManager
from src.core.location.simple_location_service import SimpleLocationService
from src.core.manager.observer_composed_objects_manager import ObserverComposedObjectsManager
from src.core.object.kvdb_moving_objects_manager import KVDBMovingObjectsManager
from src.core.object.kvdb_static_objects_manager import KVDBStaticObjectsManager
from src.core.sensor.default_sensors_manager import DefaultSensorsManager
from src.core.user.default_users_manager import DefaultUsersManager

"""
This is where we can store the dependencies needed to inject into the resources in order to properly work.

Each dependency needs to have a key for the resource to be able to find them
"""

class DependencyContainer(DeclarativeContainer):

    database = Singleton(MemoryKVDatabase)

    static_objects_manager = Singleton(KVDBStaticObjectsManager, kv_database=database)
    moving_objects_manager = Singleton(KVDBMovingObjectsManager, kv_database=database)

    objects_manager = Singleton(ObserverComposedObjectsManager,
                                observable_static_objects_manager=static_objects_manager,
                                observable_moving_objects_manager=moving_objects_manager)

    users_manager = Singleton(DefaultUsersManager, moving_objects_manager=moving_objects_manager)
    anchors_manager = Singleton(DefaultAnchorsManager, static_objects_manager=static_objects_manager)

    sensors_manager = Singleton(DefaultSensorsManager, objects_manager=objects_manager)
    signal_emitters_manager = Singleton(DefaultSignalEmittersManager, objects_manager=objects_manager)

    location_service = Singleton(SimpleLocationService)

    sensed_objects_processor = Singleton(KVDBSensedObjectsProcessor,
                                         location_service=location_service,
                                         user_manager=users_manager,
                                         sensor_manager=sensors_manager,
                                         database=database)

