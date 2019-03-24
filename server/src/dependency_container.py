from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from src.core.data.kvdb_sensed_objects_processor import KVDBSensedObjectsProcessor
from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.location.simple_location_service import SimpleLocationService
from src.core.object.kvdb_static_object_manager import KVDBStaticObject
from src.core.sensor.kvdb_sensor_manager import KVDBSensor
from src.core.user.kvdb_user_manager import KVDBUser

"""
This is where we can store the dependencies needed to inject into the resources in order to properly work.

Each dependency needs to have a key for the resource to be able to find them
"""

class DependencyContainer(DeclarativeContainer):

    database = Singleton(MemoryKVDatabase)

    user_manager = Singleton(KVDBUser, kv_database=database)
    sensor_manager = Singleton(KVDBSensor, kv_database=database)
    static_object_manager = Singleton(KVDBStaticObject, kv_database=database)

    location_service = Singleton(SimpleLocationService)

    sensed_objects_processor = Singleton(KVDBSensedObjectsProcessor, location_service=location_service,
                                         user_manager=user_manager, sensor_manager=sensor_manager, database=database)

