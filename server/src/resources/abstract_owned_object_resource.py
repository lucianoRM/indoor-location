from abc import ABCMeta, abstractmethod


class AbstractOwnedObjectResource:
    """
    Abstract resource for all objects that are owned by another object
    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def _do_get_owner(self, owner_id: str):
        raise NotImplementedError

    @abstractmethod
    def _update_owner(self, owner_id: str, owner):
        raise NotImplementedError