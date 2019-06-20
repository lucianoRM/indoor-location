from abc import ABCMeta, abstractmethod

from src.core.anchor.sensing_anchor import SensingAnchor
from src.core.anchor.signal_emitting_anchor import SignalEmittingAnchor
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.sensing_anchor_schema import SensingAnchorSchema
from src.resources.schemas.sensor_schema import SENSOR_TYPE
from src.resources.schemas.signal_emitter_schema import SIGNAL_EMITTER_TYPE
from src.resources.schemas.signal_emitting_anchor_schema import SignalEmittingAnchorSchema
from src.resources.schemas.typed_object_serializer import SerializationContext, TypedObjectSerializer

class AbstractAnchorResource(AbstractResource):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._anchors_manager = DependencyContainer.anchors_manager()
        self._serializer = TypedObjectSerializer(contexts=[
            SerializationContext(type=SENSOR_TYPE, schema=SensingAnchorSchema(strict=True), klass=SensingAnchor),
            SerializationContext(type=SIGNAL_EMITTER_TYPE, schema=SignalEmittingAnchorSchema(strict=True), klass=SignalEmittingAnchor),
        ])


class AnchorListResource(AbstractAnchorResource):
    """
    Represents anchors in the system
    """

    __custom_error_mappings = {
        'AnchorAlreadyExistsException': {
            'code': 409,
            'message': lambda e: str(e)
        }
    }

    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings, **kwargs)

    def _do_get(self):
        return self._serializer.dump(self._anchors_manager.get_all_anchors())

    def _do_post(self):
        anchor = self._serializer.load(self._get_post_data_as_json())
        return self._serializer.dump(self._anchors_manager.add_anchor(anchor_id=anchor.id, anchor=anchor))


class AnchorResource(AbstractAnchorResource):
    """
    Represents a single anchor in the system
    """

    def _do_get(self, anchor_id):
        return self._serializer.dump(self._anchors_manager.get_anchor(anchor_id=anchor_id))
