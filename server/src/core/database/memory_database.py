from .database import Database, KeyDoesNotExistException, KeyAlreadyExistsException
from copy import deepcopy


class MemoryDatabase(Database):
    CREATE_MISSING_KEYS_ARG = 'createMissingKeys'
    KEYS_DELIMITER = '.'

    def __init__(self):
        self.__database = {}

    def __get_keys(self, key):
        if (not isinstance(key, str)):
            raise TypeError("Keys must be strings")
        return key.split(self.KEYS_DELIMITER)

    def __retrieve(self, keys, createMissingKeys=False):
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
                        'The key: \'' + self.KEYS_DELIMITER.join(accessed_keys) + '\' is not present in the DB')
            elif not isinstance(tmp_value, dict) and key is not last_key:
                # in this case we should fail because we don't know how to get something from things that are not dics
                raise KeyDoesNotExistException(
                    'The key: \'' + self.KEYS_DELIMITER.join(accessed_keys) + '\' already references a leaf element, '
                                                                              'can not rerieve any further')
            current_dicc = tmp_value
        return tmp_value

    def __insert(self, key, value, createMissingKeys=False, failIfPresent=True):
        keys = self.__get_keys(key)
        last_key = keys[-1]
        last_dicc = self.__retrieve(keys[:-1:], createMissingKeys)
        if (len(last_dicc) != 0 and failIfPresent):
            raise KeyAlreadyExistsException("There is a value already associated with the key " + key)
        last_dicc[last_key] = deepcopy(value)
        return value

    def insert(self, key, value, **kwargs):
        createMissingKeys = kwargs.get(self.CREATE_MISSING_KEYS_ARG, False)
        return self.__insert(key, value, createMissingKeys=createMissingKeys, failIfPresent=True)

    def upsert(self, key, value, **kwargs):
        createMissingKeys = kwargs.get(self.CREATE_MISSING_KEYS_ARG, False)
        return self.__insert(key, value, createMissingKeys=createMissingKeys, failIfPresent=False)

    def retrieve(self, key, **kwargs):
        return deepcopy(self.__retrieve(self.__get_keys(key)))

    def remove(self, key, **kwargs):
        keys = self.__get_keys(key)
        last_key = keys[-1]
        last_dicc = self.__retrieve(keys[:-1:])
        return deepcopy(last_dicc.pop(last_key))
