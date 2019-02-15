from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.user.kvdb_user_manager import KVDBUserManager

"""
This is where we can store the dependencies needed to inject into the resources in order to properly work.

Each dependency needs to have a key for the resource to be able to find them
"""

#KEYS
USER_MANAGER = "user_manager"


#Common objects
__database = MemoryKVDatabase()


DEPENDENCY_CONTAINER = {
    USER_MANAGER : KVDBUserManager(__database)
}