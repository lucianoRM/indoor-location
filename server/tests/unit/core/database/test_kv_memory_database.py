from pytest import fixture, raises

from src.core.database.memory_kv_database import MemoryKVDatabase, KeyDoesNotExistException, KeyAlreadyExistsException


class TestMemoryDatabase:

    @fixture(autouse=True)
    def setUp(self):
        self.__database = MemoryKVDatabase()

    def test_insert_empty_key(self):
        key = ''
        value = 1
        self.__database.insert(key, value)
        assert self.__database.retrieve(key) == value

    def test_insert_none_key(self):
        key = None
        value = 1
        with raises(TypeError):
            self.__database.insert(key=key, value=value, createMissingKeys=True)

    def test_insert_value_simple_key(self):
        key = 'key'
        value = 1
        self.__database.insert(key, value)
        assert self.__database.retrieve(key) == value

    def test_insert_value_complex_key(self):
        key = self.__database.get_keys_delimiter().join(['this', 'is', 'the', 'key'])
        value = 1
        self.__database.insert(key, value, createMissingKeys=True)
        assert self.__database.retrieve(key) == value

    def test_insert_complex_key_missing_flag(self):
        key = self.__database.get_keys_delimiter().join(['this', 'is', 'the', 'key'])
        value = 1
        with raises(KeyDoesNotExistException):
            self.__database.insert(key=key, value=value, createMissingKeys=False)

    def test_insert_already_existing_simple_key(self):
        key = 'key'
        value = 1
        self.__database.insert(key, value)
        with raises(KeyAlreadyExistsException):
            self.__database.insert(key=key, value=value)

    def test_insert_already_existing_complex_key(self):
        key = self.__database.get_keys_delimiter().join(['this', 'is', 'the', 'key'])
        value = 1
        self.__database.insert(key, value, createMissingKeys=True)
        with raises(KeyAlreadyExistsException):
            self.__database.insert(key=key, value=value)

    def test_upsert_missing_simple_key(self):
        key = 'key'
        value = 1
        self.__database.upsert(key, value)
        assert self.__database.retrieve(key) == value

    def test_upsert_missing_complex_key(self):
        key = self.__database.get_keys_delimiter().join(['this', 'is', 'the', 'key'])
        value = 1
        self.__database.upsert(key, value, createMissingKeys=True)
        assert self.__database.retrieve(key) == value

    def test_upsert_existing_simple_key(self):
        key = 'key'
        value = 1
        value2 = 2
        self.__database.insert(key, value)
        self.__database.upsert(key, value2)
        assert self.__database.retrieve(key) == value2

    def test_upsert_existing_complex_key(self):
        key = self.__database.get_keys_delimiter().join(['this', 'is', 'the', 'key'])
        value = 1
        value2 = 2
        self.__database.insert(key, value, createMissingKeys=True)
        self.__database.upsert(key, value2, createMissingKeys=True)
        assert self.__database.retrieve(key) == value2

    def test_insert_complex_update_simple(self):
        keylist = ['this', 'is', 'the', 'key']
        key = self.__database.get_keys_delimiter().join(keylist)
        key1 = self.__database.get_keys_delimiter().join(keylist[:-1:])  # this.is.the
        key2 = self.__database.get_keys_delimiter().join(keylist[:-2:])  # this.is
        key3 = self.__database.get_keys_delimiter().join(keylist[:-3:])  # this
        value = 1
        value2 = 2
        self.__database.insert(key, value, createMissingKeys=True)
        self.__database.upsert(key3, value2, createMissingKeys=True)
        with raises(KeyDoesNotExistException):
            self.__database.retrieve(key=key)
        with raises(KeyDoesNotExistException):
            self.__database.retrieve(key=key1)
        with raises(KeyDoesNotExistException):
            self.__database.retrieve(key=key2)
        assert self.__database.retrieve(key3) == value2

    def test_update_missing_simple_key(self):
        with raises(KeyDoesNotExistException):
            self.__database.update(key="somekey",value="somevalue", createMissingKeys=False)

    def test_update_missing_complex_key(self):
        key = self.__database.get_keys_delimiter().join(['this', 'is', 'the', 'key'])
        with raises(KeyDoesNotExistException):
            self.__database.update(key=key,value="somevalue",createMissingKeys=False)

    def test_update_with_simple_key(self):
        key = "thekey"
        value = "initialValue"
        self.__database.insert(key, value)
        assert self.__database.retrieve(key) == value
        newValue = "newValue"
        self.__database.update(key, newValue)
        assert self.__database.retrieve(key) == newValue

    def test_update_with_complex_key(self):
        key = self.__database.get_keys_delimiter().join(['this', 'is', 'the', 'key'])
        value = "initialValue"
        self.__database.insert(key, value)
        assert self.__database.retrieve(key) == value
        newValue = "newValue"
        self.__database.update(key, newValue)
        assert self.__database.retrieve(key) == newValue

    def test_upsert_complex_missing_flag(self):
        key = self.__database.get_keys_delimiter().join(['this', 'is', 'the', 'key'])
        value = 1
        with raises(KeyDoesNotExistException):
            self.__database.upsert(key=key,value=value, createMissingKeys=False)

    def test_value_is_immutable_simple_key(self):
        key = 'key'
        value = 1
        self.__database.insert(key, value, createMissingKeys=True)
        value = 2
        assert self.__database.retrieve(key) != value

    def test_value_is_immutable_complex_key(self):
        key = self.__database.get_keys_delimiter().join(['this', 'is', 'the', 'key'])
        value = 1
        self.__database.insert(key, value, createMissingKeys=True)
        value = 2
        assert self.__database.retrieve(key) != value

    def test_insert_key_not_string(self):
        key = ['key']
        value = 1
        with raises(TypeError):
            self.__database.insert(key=key,value=value, createMissingKeys=True)

    def test_insert_non_dicc_value_as_leaf(self):
        key = self.__database.get_keys_delimiter().join(['this', 'is', 'the', 'key'])
        value = ['this','is','the','value']
        self.__database.insert(key, value, createMissingKeys=True)
        assert self.__database.retrieve(key=key) == value

    def test_insert_non_dicc_value_retrieve_deeper_value(self):
        keylist = ['this', 'is', 'the', 'key']
        insert_key = self.__database.get_keys_delimiter().join(keylist)
        keylist.append('newword')
        retrieve_key = self.__database.get_keys_delimiter().join(keylist)
        value = ['this','is','the','value']
        self.__database.insert(insert_key, value, createMissingKeys=True)
        with raises(KeyDoesNotExistException):
            self.__database.retrieve(key=retrieve_key)

    def test_remove_simple_key(self):
        key = 'key'
        value = 1
        self.__database.insert(key, value)
        self.__database.remove(key)
        with raises(KeyDoesNotExistException):
            self.__database.retrieve(key=key)

    def test_insert_complex_key_remove_simple(self):
        keylist = ['this', 'is', 'the', 'key']
        insert_key = self.__database.get_keys_delimiter().join(keylist)
        retrieve_key3 = self.__database.get_keys_delimiter().join(keylist[:-1:]) #this.is.the
        retrieve_key2 = self.__database.get_keys_delimiter().join(keylist[:-2:]) #this.is
        remove_key = self.__database.get_keys_delimiter().join(keylist[:-3:]) #this
        value = 1
        self.__database.insert(insert_key, value, createMissingKeys=True)
        self.__database.remove(remove_key)
        with raises(KeyDoesNotExistException):
            self.__database.retrieve(key=retrieve_key3)
        with raises(KeyDoesNotExistException):
            self.__database.retrieve(key=retrieve_key2)
        with raises(KeyDoesNotExistException):
            self.__database.retrieve(key=insert_key)


    def test_insert_remove_complex_key(self):
        keylist = ['this', 'is', 'the', 'key']
        insert_key = self.__database.get_keys_delimiter().join(keylist)
        retrieve_key3 = self.__database.get_keys_delimiter().join(keylist[:-1:]) #this.is.the
        retrieve_key2 = self.__database.get_keys_delimiter().join(keylist[:-2:]) #this.is
        retrieve_key1 = self.__database.get_keys_delimiter().join(keylist[:-3:]) #this
        value = 1
        self.__database.insert(insert_key, value, createMissingKeys=True)
        self.__database.remove(insert_key)
        assert self.__database.retrieve(key=retrieve_key1) is not None
        assert self.__database.retrieve(key=retrieve_key2) is not None

        assert len(self.__database.retrieve(retrieve_key3)) == 0
        with raises(KeyDoesNotExistException):
            self.__database.retrieve(key=insert_key)


