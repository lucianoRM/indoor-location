from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from src.core.data.kvdb_sensed_objects_processor import KVDBSensedObjectsProcessor
from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.sensor.kvdb_sensor_manager import KVDBSensorManager
from src.core.user.kvdb_user_manager import KVDBUserManager

"""
This is where we can store the dependencies needed to inject into the resources in order to properly work.

Each dependency needs to have a key for the resource to be able to find them
"""

class DependencyContainer(DeclarativeContainer):

    database = Singleton(MemoryKVDatabase)
    user_manager = Singleton(KVDBUserManager, kv_database=database)
    sensor_manager = Singleton(KVDBSensorManager, kv_database=database)
    sensed_objects_processor = Singleton(KVDBSensedObjectsProcessor, user_manager=user_manager, sensor_manager=sensor_manager, database=database)
