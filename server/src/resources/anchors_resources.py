from abc import ABCMeta, abstractmethod

from src.core.data.sensed_objects_processor import SensedObjectsProcessor
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.anchor_schema import AnchorSchema
from src.resources.schemas.serializer import Serializer
from src.resources.sensors_resources import OwnedSensorListResource, OwnedSensorResource
from src.resources.signal_emitters_resources import OwnedSignalEmitterListResource, OwnedSignalEmitterResource


class AbstractAnchorResource(AbstractResource):
    __metaclass__ = ABCMeta

    __custom_error_mappings = {
        'AnchorAlreadyExistsException': {
            'code': 409,
            'message': lambda e: str(e)
        },
        'SensorAlreadyExistsException': {
            'code': 409,
            'message': lambda e: str(e)
        },
        'SignalEmitterAlreadyExistsException': {
            'code': 409,
            'message': lambda e: str(e)
        },
        'UnknownAnchorException': {
            'code': 404,
            'message': lambda e: str(e)
        },
        'UnknownSensorException': {
            'code': 404,
            'message': lambda e: str(e)
        },
        'UnknownSignalEmitterException': {
            'code': 404,
            'message': lambda e: str(e)
        }
    }

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(custom_error_mappings=self.__custom_error_mappings, **kwargs)
        self._anchors_manager = DependencyContainer.anchors_manager()
        self._anchor_serializer = Serializer(AnchorSchema(strict=True))
        self._sensed_objects_processor = DependencyContainer.sensing_anchor_object_processor()

    def _do_get_processor(self) -> SensedObjectsProcessor:
        return self._sensed_objects_processor

    def _do_get_owner(self, owner_id: str):
        return self._anchors_manager.get_anchor(owner_id)

    def _update_owner(self, owner_id: str, owner):
        self._anchors_manager.update_anchor(owner_id, owner)


class AnchorListResource(AbstractAnchorResource):
    """
    Represents anchors in the system
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _do_get(self):
        return self._anchor_serializer.serialize(self._anchors_manager.get_all_anchors())

    def _do_post(self):
        anchor = self._anchor_serializer.deserialize(self._get_post_data_as_json())
        return self._anchor_serializer.serialize(self._anchors_manager.add_anchor(anchor_id=anchor.id, anchor=anchor))

class AnchorResource(AbstractAnchorResource):
    """
    Represents a single anchor in the system
    """

    def _do_get(self, anchor_id):
        return self._anchor_serializer.serialize(self._anchors_manager.get_anchor(anchor_id=anchor_id))

    def _do_delete(self, anchor_id):
        return self._anchor_serializer.serialize(self._anchors_manager.remove_anchor(anchor_id=anchor_id))


class SensingAnchorSensorListResource(AbstractAnchorResource, OwnedSensorListResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SensingAnchorSensorResource(AbstractAnchorResource, OwnedSensorResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SignalEmittingAnchorSEListResource(AbstractAnchorResource, OwnedSignalEmitterListResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SignalEmittingAnchorSEResource(AbstractAnchorResource, OwnedSignalEmitterResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
