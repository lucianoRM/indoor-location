

from src.core.anchor.sensing_anchor import SensingAnchor
from src.core.anchor.signal_emitting_anchor import SignalEmittingAnchor
from src.core.sensor.sensor import Sensor
from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.typed_object_schema import TypedObjectSchema


class AnchorListResource(AbstractResource):
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
        self.__anchors_manager = DependencyContainer.anchors_manager()
        self.__anchors_schema = AnchorSchema(many=True, strict=True)
        self.__anchor_schema = AnchorSchema(strict=True)

    def _do_get(self):
        return self.__anchors_schema.dump(self.__anchors_manager.get_all_anchors())

    def _do_post(self):
        anchor = self.__anchor_schema.load(self._get_post_data_as_json()).data
        return self.__anchor_schema.dump(self.__anchors_manager.add_anchor(anchor_id=anchor.id, anchor=anchor))


class AnchorResource(AbstractResource):
    """
    Represents a single anchor in the system
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__anchors_manager = DependencyContainer.anchors_manager()
        self.__anchor_schema = AnchorSchema(strict=True)

    def _do_get(self, anchor_id):
        return self.__anchor_schema.dump(self.__anchors_manager.get_anchor(anchor_id=anchor_id))


class AnchorSchema(TypedObjectSchema):

    __SENSOR_TYPE = "SENSOR"
    __SIGNAL_EMITTER_TYPE = "SIGNAL_EMITTER"

    def _get_valid_types(self):
        return [self.__SENSOR_TYPE, self.__SIGNAL_EMITTER_TYPE]

    def _do_make_object(self, type, kwargs):
        if type == self.__SENSOR_TYPE:
            return SensingAnchor(**kwargs)
        else:
            return SignalEmittingAnchor(**kwargs)

    def _get_object_type(self, original_object):
        if isinstance(original_object, Sensor):
            return self.__SENSOR_TYPE
        else:
            return self.__SIGNAL_EMITTER_TYPE