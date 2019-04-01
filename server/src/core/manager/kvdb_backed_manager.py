from abc import ABCMeta


class KVDBBackedManager:
    """
    Parent class that handles values when stored in a key-value database
    """
    __metaclass__ = ABCMeta

    def __init__(self, kv_database, **kwargs):
        self._database = kv_database
        super().__init__(**kwargs)

    def _build_complex_key(self, *args):
        return self._database.get_keys_delimiter().join(args)