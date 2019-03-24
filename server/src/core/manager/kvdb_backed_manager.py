from abc import ABCMeta


class KVDBBacked(object):
    """
    Parent class that handles values when stored in a key-value database
    """
    __metaclass__ = ABCMeta

    def __init__(self, KVDatabase):
        self._database = KVDatabase

    def _build_complex_key(self, *args):
        return self._database.get_keys_delimiter().join(args)