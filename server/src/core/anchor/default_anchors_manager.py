from typing import List

from src.core.anchor.anchor import Anchor
from src.core.anchor.anchors_manager import AnchorsManager, AnchorAlreadyExistsException, UnknownAnchorException
from src.core.object.static_objects_manager import StaticObjectsManager, StaticObjectAlreadyExistsException, UnknownStaticObjectException

class DefaultAnchorsManager(AnchorsManager):

    def __init__(self, static_objects_manager: StaticObjectsManager):
        self.__static_objects_manager = static_objects_manager
        super().__init__()

    def add_anchor(self, anchor_id: str, anchor: Anchor) -> Anchor:
        try:
            return self.__static_objects_manager.add_static_object(object_id=anchor_id, object=anchor)
        except StaticObjectAlreadyExistsException:
            raise AnchorAlreadyExistsException("Anchor with id " + anchor_id + " was already registered")

    def get_anchor(self, anchor_id: str) -> Anchor:
        try:
            return self.__static_objects_manager.get_static_object(object_id=anchor_id)
        except UnknownStaticObjectException:
            raise UnknownAnchorException("Anchor with id " + anchor_id + " was never registered")

    def remove_anchor(self, anchor_id: str) -> Anchor:
        try:
            return self.__static_objects_manager.remove_static_object(object_id=anchor_id)
        except UnknownStaticObjectException:
            raise UnknownAnchorException("No anchor with id " + anchor_id + " exists")

    def update_anchor(self, anchor_id: str, anchor: Anchor) -> Anchor:
        try:
            return self.__static_objects_manager.update_static_object(object_id=anchor_id, object=anchor)
        except UnknownStaticObjectException:
            raise UnknownAnchorException("There is no anchor with id " + anchor_id + " to update")

    def get_all_anchors(self) -> List[Anchor]:
        return self.__static_objects_manager.get_all_static_objects()


