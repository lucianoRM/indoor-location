from src.core.anchor.sensing_anchor import SensingAnchor
from src.core.user.sensing_user import SensingUser
from src.core.user.user import User
from src.resources.schemas.typed_object_schema import TypedObjectSchema


class SensorSchema(TypedObjectSchema):

    __USER_TYPE = "USER"
    __ANCHOR_TYPE = "ANCHOR"

    def _get_valid_types(self):
        return [self.__USER_TYPE, self.__ANCHOR_TYPE]

    def _do_make_object(self, type, kwargs):
        if type == self.__USER_TYPE:
            return SensingUser(**kwargs)
        else:
            return SensingAnchor(**kwargs)

    def _get_object_type(self, original_object):
        if isinstance(original_object, User):
            return self.__USER_TYPE
        else:
            return self.__ANCHOR_TYPE