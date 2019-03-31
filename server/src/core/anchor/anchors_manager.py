from abc import ABCMeta, abstractmethod
from typing import List

from src.core.anchor.anchor import Anchor


class AnchorsManager:
    """
    API for handling Anchors
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_anchor(self, anchor_id: str, anchor: Anchor) -> Anchor:
        """
        Add a new anchor
        :param anchor_id: the id to store the anchor
        :param anchor: the anchor to add
        :raise AnchorAlreadyExistsException: if the anchor was already added
        :return: the anchor added
        """
        raise NotImplementedError

    @abstractmethod
    def get_anchor(self, anchor_id: str) -> Anchor:
        """
        Get the anchor with anchor_id
        :param anchor_id: the id that uniquely identifies that anchor
        :return: An anchor with id: anchor_id
        """
        raise NotImplementedError

    @abstractmethod
    def remove_anchor(self, anchor_id: str) -> Anchor:
        """
        Remove an anchor by id
        :param anchor_id: The id to uniquely locate the anchor to remove
        :raise: UnkownAnchorException: If the anchor is not found
        :return: The anchor with the given id
        """
        raise NotImplementedError

    @abstractmethod
    def update_anchor(self, anchor_id: str, anchor: Anchor) -> Anchor:
        """
        Update an already existent anchor.
        :param anchor_id: The id of the anchor to be updated
        :param anchor: The new anchor that will replace the old one with new information
        :raise: UnknownAnchorException if no anchor is found with the given id.
        :return: The new anchor updated
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_anchors(self) -> List[Anchor]:
        """
        Return all registered anchors
        :return: all anchors
        """
        raise NotImplementedError



class AnchorsManagerException(Exception):
    """
    Root exception related to an AnchorsManager
    """


class AnchorAlreadyExistsException(AnchorsManagerException):
    """
    Throw this exception when wanting to add an anchor that already exists
    """
    pass


class UnknownAnchorException(AnchorsManagerException):
    """
    Throw this exception when the requested anchor is not found
    """
    pass