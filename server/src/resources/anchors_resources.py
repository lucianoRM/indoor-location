from abc import ABCMeta, abstractmethod

from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.anchor_schema import AnchorSchema
from src.resources.schemas.serializer import Serializer

class AbstractAnchorResource(AbstractResource):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._anchors_manager = DependencyContainer.anchors_manager()
        self._serializer = Serializer(AnchorSchema(strict=True))


class AnchorListResource(AbstractAnchorResource):
    """
    Represents anchors in the system
    """

    __custom_error_mappings = {
        'AnchorAlreadyExistsException': {
            'code': 409,
            'message': lambda e: str(e)
        },
        'SensorAlreadyExistsException': {
            'code': 400,
            'message': lambda e: str(e)
        },
        'SignalEmitterAlreadyExistsException': {
            'code': 400,
            'message': lambda e: str(e)
        }
    }

    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings, **kwargs)

    def _do_get(self):
        return self._serializer.serialize(self._anchors_manager.get_all_anchors())

    def _do_post(self):
        anchor = self._serializer.deserialize(self._get_post_data_as_json())
        return self._serializer.serialize(self._anchors_manager.add_anchor(anchor_id=anchor.id, anchor=anchor))


class AnchorResource(AbstractAnchorResource):
    """
    Represents a single anchor in the system
    """

    def _do_get(self, anchor_id):
        return self._serializer.serialize(self._anchors_manager.get_anchor(anchor_id=anchor_id))
