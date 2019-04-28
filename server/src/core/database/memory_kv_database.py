
from copy import deepcopy
from typing import List, Generic, TypeVar

from src.core.database.kv_database import KeyDoesNotExistException, KVDatabase, KeyAlreadyExistsException

T = TypeVar('T')

class MemoryKVDatabase(KVDatabase):
    """
    Key-value database implementation that keeps information stored in a dictionary.
    """

    __CREATE_MISSING_KEYS_ARG = 'createMissingKeys'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__database = {}

    def __get_keys(self, key: str) -> List[str]:
        if not isinstance(key, str):
            raise TypeError("Keys must be strings")
        return key.split(self.get_keys_delimiter())

    def __has_key(self, key: str) -> bool:
        try:
            self.__retrieve(self.__get_keys(key))
            return True
        except KeyDoesNotExistException:
            return False

    def __retrieve(self, keys: List[str], createMissingKeys=False):
        current_dicc = self.__database
        tmp_value = self.__database
        accessed_keys = []
        last_key = None if not keys else keys[-1]
        for key in keys:
            accessed_keys.append(key)
            tmp_value = current_dicc.get(key)
            if tmp_value is None:
                if createMissingKeys:
                    tmp_value = {}
                    current_dicc[key] = tmp_value
                else:
                    raise KeyDoesNotExistException(
                        'The key: \'' + self.get_keys_delimiter().join(accessed_keys) + '\' is not present in the DB')
            elif not isinstance(tmp_value, dict) and key is not last_key:
                # in this case we should fail because we don't know how to get something from things that are not dics
                raise KeyDoesNotExistException(
                    'The key: \'' + self.get_keys_delimiter().join(accessed_keys) + '\' already references a leaf element, '
                                                                              'can not rerieve any further')
            current_dicc = tmp_value
        return tmp_value

    def __insert(self, key: str, value: Generic[T], createMissingKeys=False, failIfPresent=True) -> T:
        keys = self.__get_keys(key)
        last_key = keys[-1]
        last_dicc = self.__retrieve(keys[:-1:], createMissingKeys)
        if last_key in last_dicc and failIfPresent:
            raise KeyAlreadyExistsException("There is a value already associated with the key " + key)
        last_dicc[last_key] = deepcopy(value)
        return value

    def insert(self, key: str, value: Generic[T], **kwargs) -> T:
        createMissingKeys = kwargs.get(self.__CREATE_MISSING_KEYS_ARG, True)
        return self.__insert(key, value, createMissingKeys=createMissingKeys, failIfPresent=True)

    def update(self, key: str, value: Generic[T], **kwargs) -> T:
        if self.__has_key(key):
            return self.upsert(key, value, createMissingKeys=False, failIfPresent=False)
        raise KeyDoesNotExistException("The key: " + key + " does not exists in the DB")

    def upsert(self, key: str, value: Generic[T], **kwargs) -> T:
        createMissingKeys = kwargs.get(self.__CREATE_MISSING_KEYS_ARG, True)
        return self.__insert(key, value, createMissingKeys=createMissingKeys, failIfPresent=False)

    def retrieve(self, key: str, **kwargs) -> T:
        return deepcopy(self.__retrieve(self.__get_keys(key)))

    def remove(self, key: str, **kwargs) -> T:
        keys = self.__get_keys(key)
        last_key = keys[-1]
        last_dicc = self.__retrieve(keys[:-1:])
        return deepcopy(last_dicc.pop(last_key))
